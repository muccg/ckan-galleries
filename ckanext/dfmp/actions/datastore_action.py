import ckan.plugins.toolkit as toolkit
from ckan.logic import side_effect_free
from ckanext.dfmp.bonus import _validate, _unjson, _unjson_base, _get_package_id_by_res, _sanitize
from ckan.lib.helpers import url_for
import ckan.model as model
from random import randint
import logging, requests, json
from dateutil.parser import parse

from pylons import config

from ckanext.dfmp.actions.action import indexer, searcher
import ckanext.dfmp.dfmp_solr as solr
from ckanext.dfmp.dfmp_solr import _asset_search
from ckanext.dfmp.asset import Asset
log = logging.getLogger(__name__)
session = model.Session

DEF_LIMIT = 21
DEF_FIELDS = '_id, CAST("assetID" AS TEXT), CAST(url AS TEXT), CAST("lastModified" AS TEXT), metadata, name, spatial'

@side_effect_free
def resource_items(context, data_dict):
  '''
  Returns items from asset if only {id} specified or single item
  if {item} specified as well. Also you can use {limit} and {offset} 
  for global search
  '''
  _validate(data_dict, 'id')
  id = data_dict['id']

  item = data_dict.get('item')
  if item:
    result = Asset.get(id, item, context=context)

  else:
    limit = int(data_dict.get('limit', 21))
    offset = int(data_dict.get('offset', 0)) 
    result = Asset.get_all(data_dict['id'], limit, offset, context=context)
  package_id = session.query(model.Resource).filter_by(id=id).first().get_package_id()

  result['backlink'] = url_for(controller='package', action='resource_read', resource_id=id, id=package_id)[1:]
  package = toolkit.get_action('package_show')(context, {'id':package_id})

  result['count'] = solr.DFMPSearchQuery.run({
    'q':'id:({ids})'.format(ids=id),
    'fq':'-state:hidden',
    'rows':0,
  })['count']
  organization = package['organization']
  if organization:
    organization['dfmp_link'] = config.get('ckan.site_url') + '/organization/{name}'.format(name=organization['name'])

    pkgs = session.query(model.Package).filter(
      model.Package.owner_org == organization['id'],
      model.Package.private == False,
      model.Package.state == 'active'
    ).all()

    all_res = []
    for pkg in pkgs:
      for res in pkg.resources:
        all_res.append(res.id)
    ids = ' OR '.join(all_res)
    ammount = solr.DFMPSearchQuery.run({
      'q':'id:({ids})'.format(ids=ids),
      'fq':'-state:hidden',
      'rows':0,
    })['count']
    organization['dfmp_assets'] = ammount
  result['organization'] = organization
  if result['records']:
    result['records'][0]['organization'] = organization
  result['title'] = package.get('title')
  result['description'] = package.get('notes')
  result['tags'] = ','.join([item['display_name'] for item in package.get('tags')])
  return result

 

@side_effect_free
def static_gallery_reset(context, data_dict):
  '''
  Deprecated
  '''
  return

@side_effect_free
def dfmp_static_gallery(context, data_dict):
  '''
  Returns random items from gallery
  '''
  ammount = searcher({
    'q':'',
    'fq':'-state:hidden',
    'rows':0,
  })['count']
  limit = int( data_dict.get('limit', 21) )

  offset = randint (0, ammount - limit - 1)

  result = _asset_search(**{
    'q':'',
    'fq':'-state:hidden', 
    'limit':limit,
    'offset':offset,
  })
  records = []
  for item in result['results']:
    try:
      json_str = item['data_dict']
      json_dict = json.loads(json_str)
      records.append(json_dict)
    except:
      pass
  return records

@side_effect_free
def dfmp_all_assets(context, data_dict):
  limit = int(data_dict.get('limit', 8))
  offset = int(data_dict.get('offset', 0))
  result = searcher({
    'q':'',
    'facet.field':'id',
    'rows':0,
  })
  ids = result['facets']['id'].keys()[offset:offset+limit]
  response = []
  for item in ids:
    try:
      package_id = _get_package_id_by_res(item)
    except AttributeError, e:
      log.warn(e)
      log.warn('Package not exists')
      continue
    package = toolkit.get_action('package_show')( 
      context,
      {'id':package_id}
    )
    package['asset'] = filter(lambda x: x['id'] == item, package['resources'])[0]
    del package['resources']
    dfmp_img = searcher({
      'q':'id:{id}'.format(id=item),
      'fl':'url',
      'fq':'+url:http*',
      'rows':1,
    })
    package['dfmp_img'] = dfmp_img['results'].pop() if len(dfmp_img['results']) else {'url':''}
    if not package['dfmp_img']['url'].startswith('http') or requests.head( package['dfmp_img']['url'] ).status_code != 200:
      package['dfmp_img'] = {'url':'http://lorempixel.com/300/300/'}

    package['dfmp_total']=dfmp_img['count']
    package['tags'] = [tag['display_name'] for tag in package['tags']]
    package['dfmp_site_assets_ammount']=result['count']
    package['dfmp_site_resources_ammount']=len(result['facets']['id'])

    package['dataset_link']=url_for(controller='package', action='read', id=package_id)
    package['asset_link'] = package['dataset_link'] + '/resource/{res}'.format(res=item)

    response.append(package)
    if len(response) >= limit:
      break

  return response

@side_effect_free
def search_item(context, data_dict):
  '''
  Search by name, tags, type, from date
  '''
  _validate(data_dict, 'query_string')
  user_query = data_dict['query_string']
  search_query = { 
    'facet_fields': [
      'organization',
      'tags',
      'license_id'
    ]
  }
  fq = query = ''

  try: limit = int(data_dict['limit'])
  except: limit = 21
  try: offset = int(data_dict['offset'])
  except: offset = 0
  search_query.update(limit=limit, offset=offset)

  atype = user_query.get('type') or ''
  if atype:
    if atype == 'cc':
      atype = ' +license_id:{type}*'.format(type=atype)
    else:
      atype = ' +(extras_mimetype:{type}* OR extras_type:{type}*)'.format(type=atype)

  tags = user_query.get('tags') or ''
  if type(tags) in (str, unicode):
    tags = [tag.strip() for tag in tags.split(',') if tag]
  tags = ' +tags:({tags})'.format(tags = ' AND '.join(tags)) if tags else ''

  include_description = user_query.get('include_description')
  name = user_query.get('name') or ''
  if name:
    if include_description:
      name += '(name:{name} OR text:{name})'.format(name = name)
    else:
      name = 'name:{name}'.format(name = name)
    
  
  license = user_query.get('licence') or ''
  if license:
    license = ' +license_id:{license}*'.format(license=license)
  
  date = user_query.get('date')
  try:
    date = '+metadata_modified:[{start} TO *]'.format(
      start= parse(date).isoformat() + 'Z'
    )
  except ValueError: date = ''
  except AttributeError: date = ''

  query = '{name} {date} {tags} {type} {license}'.format(
    name = name,
    date = date,
    tags = tags,
    type = atype,
    license = license
  )

  if query.strip():
    search_query.update(q=query)

  if fq.strip():
    search_query.update(fq=fq)
  result = _asset_search(**search_query)
  records = []
  for item in result['results']:
    try:
      json_str = item['data_dict']
      json_dict = json.loads(json_str)
      records.append(json_dict)
    except:
      pass
  del result['results']

  result.update(records=records, limit=limit, offset=offset)
  return result