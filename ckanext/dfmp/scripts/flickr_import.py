import flickrapi, math, json, uuid, logging, ckanapi, string
import ckan.plugins.toolkit as toolkit
from datetime import datetime
from ckanext.dfmp.bonus import _name_normalize

log = logging.getLogger(__name__)
from pylons import config


# FLICKR INIT
api_key = u'1903a21d2f1e99652164ad8c681e4b22'
api_secret = u'34ed321a99cb93f6'
flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')

# Harvesting options
photos_per_iteration = 100.

# updates single resource
def flickr_group_pool_resource_update (context, resource_id):
  datastore = toolkit.get_action('resource_show')(context, {'id': resource_id})
  data = {'datastore': datastore}
  toolkit.get_action('celery_flickr_import')(context, data)


# group not found action
def group_not_found(type, message):
  # CODE THAT SAYS USER THAT URL IS INCORRECT AND GROUP NOT FOUND
  import ckan.plugins.toolkit as toolkit

  raise getattr(toolkit, type)(message)

# generates package name
def _flickr_dataset_name_generate(dataset):
  return u"flickr_pool_" + (dataset[u"path_alias"] or _name_normalize(dataset[u"group_id"]))

# return appropriate datastore
def flickr_group_pool_get_datastore(context, dataset, group_id):
  # Checks resources for dataset
  package_id = dataset['name']
  package = context['session'] \
    .query(context['model'].Package) \
    .filter_by(name=package_id) \
    .first()

  # creates resource if it is not created yet
  if not package.resources:
    datastore_id = group_id
    datastore = toolkit.get_action('resource_create')(context, {
      'package_id': package_id,
      'id': datastore_id,
      'url': config.get('ckan.site_url') + '/datastore/dump/' + datastore_id,
      'name': dataset['name'].replace('flickr_', ''),
      'resource_type': 'asset'
    })
  else:
    datastore = toolkit.get_action('resource_show')(context, {'id': package.resources[0].id})

  # creates datastore if not exists
  if datastore.get('datastore_active'):
    pass
  else:
    toolkit.get_action('datastore_create')(context, {
      'resource_id': datastore['id'],
      'force': True,
      'fields': [
        {'id': 'assetID', 'type': 'text'},
        {'id': 'lastModified', 'type': 'text'},
        {'id': 'name', 'type': 'text'},
        {'id': 'url', 'type': 'text'},
        {'id': 'spatial', 'type': 'json'},
        {'id': 'metadata', 'type': 'json'},
      ],
      'primary_key': ['assetID'],
      'indexes': ['name', 'assetID']
      })

  return datastore

# creates dataset
def flickr_group_pool_create_dataset(context, dataset):
  group_id = dataset[u"group_id"]

  try:
    package = toolkit.get_action('package_create')(context, {
      'name': _flickr_dataset_name_generate(dataset),
      'title': u"Flickr - " + dataset[u"name"],
      'notes': dataset[u"description"],
      'tags': []
    })
  except toolkit.ValidationError, e:
    package = toolkit.get_action('package_show')(context, {'id': _flickr_dataset_name_generate(dataset)})
    datastore = flickr_group_pool_get_datastore(context, package, group_id)

    return package, True, datastore

  try:
    toolkit.get_action('package_owner_org_update')(context, {
      'id': package['id'],
      'organization_id': 'brand-cbr'
    })
  except Exception:
    log.warn('Error during adding user to organization ')

  datastore = flickr_group_pool_get_datastore(context, package, group_id)

  return package, False, datastore




# adds resource to dataset
def flickr_group_pool_add_resource(context, resources, datastore):
  # organization = _organization_from_list(context['auth_user_obj'].get_groups())[2]
  # data_dict['owner_name'] = organization.title  if organization else context['auth_user_obj'].name

  # ckan api init
  ckan = ckanapi.RemoteCKAN(
    context['site_url'],
    context['apikey'],
  )

  # collects records for dataset
  records = []

  # prepares resources
  for resource in resources:
    # Gets spatial coords if they exist
    if resource[u"spatial"][u"latitude"] and resource[u"spatial"][u"longitude"]:
      location = {
        "type": "Point",
        "coordinates": [
          float(resource[u"spatial"][u"longitude"]),
          float(resource[u"spatial"][u"latitude"])
        ]
      }
    else:
      location = None

    # Gets resource license
    if resource[u"metadata"][u"license"]:
      resource['license_name'] = resource[u"metadata"][u"license"]

    records.append({
      'assetID': resource[u"metadata"][u"flickr_id"],
      'lastModified': datetime.fromtimestamp(int(resource[u"dateadded"])).isoformat(' '),
      'name': resource[u"name"],
      'url': resource[u"url"],
      'spatial': location,
      'metadata': resource[u"metadata"]
    })

  # adds item to datastore
  datastore_items = ckan.call_action('datastore_upsert', {
    'resource_id': datastore['id'],
    'force': True,
    'records': records,
    'method': 'upsert'
  })

  return datastore_items


# get existing original url
def flickr_group_pull_get_existing_correct_url(resource, reversed=False):
  # url priority
  urls = (u"url_o", u"url_l", u"url_c", u"url_z", u"url_n", u"url_m", u"url_q", u"url_s", u"url_t", u"url_sq")

  # the order should be reversed for thumbbail URL
  if reversed:
    urls = urls[::-1]

  # finds the most appropriate path from existing one
  image_path = ''
  for path in urls:
    if (resource.get(path)):
      image_path = resource[path]
      break

  return image_path


def flickr_group_pool_add_images_to_dataset(context, data):
  context = json.loads(context)
  datastore = data['datastore']

  # gets the list of marked/forbidden items
  forbidden_items = datastore.get('forbidden_id', [])

  # We get the total number of photos in the pool here
  photos = flickr.groups.pools.getPhotos(group_id=datastore['id'], per_page=1, page=1)

  rough_total = int(photos[u"photos"][u"total"])

  # counting the number of iterations
  number_of_iterations = math.ceil(rough_total / photos_per_iteration)

  # counter init
  total = 0

  ckan = ckanapi.RemoteCKAN(
    context['site_url'],
    context['apikey'],
  )

  for iteration in range(1, int(number_of_iterations) + 1):
    batch = flickr.groups.pools.getPhotos(group_id=datastore['id'], per_page=photos_per_iteration, page=iteration,
                                          extras=u"description, license, original_format, geo,tags, machine_tags, url_sq, url_t, url_s, url_q, url_m, url_n, url_z, url_c, url_l, url_o, owner_name")

    # collects resources
    resources = []

    # process each photo
    for photo in batch[u"photos"][u"photo"]:

      # don't update forbidden assets
      if photo[u"id"] in forbidden_items:
        continue

      # fetches resource data
      resources.append({
        u"name": photo.get(u"title", photo[u"title"]),
        # gets first available url
        u"url": flickr_group_pull_get_existing_correct_url(photo),
        u"dateadded": photo[u"dateadded"],
        u"spatial": {
          u"latitude": photo.get(u"latitude"),
          u"longitude": photo.get(u"longitude"),
        },
        u"metadata": {
          u"post_url": 'https://www.flickr.com/photos/' + photo[u"owner"] + '/' + photo[u"id"] if photo.get(u"owner") and photo.get(u"id") else None,
          u"mimetype": u"image/" + photo.get(u"originalformat", ''),
          # gets first available url
          u"thumb": flickr_group_pull_get_existing_correct_url(photo, reversed=True),
          u"text": photo[u"description"][u"_content"],
          u"time": photo.get(u"dateadded"),
          u"name": photo.get(u"title"),
          u"tags": ','.join(photo[u"tags"].split(' ')) if photo.get(u"tags") else "",
          u"machine_tags": photo.get(u"machine_tags"),
          u"license": photo.get(u"license"),
          u"flickr_id": photo.get(u"id"),
          u"source": u"flickr",
          u"owner": photo.get(u"owner"),
          u"owner_name": photo.get(u"ownername")
        }
      })

      # updates counter
      total += 1

    # adds resources to dataset
    flickr_group_pool_add_resource(context, resources, datastore)

    # update job status
    task_status = {
      'entity_id': datastore['id'],
      'task_type': 'flickr_import',
      'key': 'celery_task_id',
      'value': str(total) + ' images has already been imported. Approximate total number of images is ' + str(rough_total),
      'state': total,
      'error': u'',
      'last_updated': datetime.now().isoformat(' '),
      'entity_type': 'resource'
    }
    update = ckan.call_action(
      'task_status_update',
      task_status
    )

  # update job status
  task_status = {
    'entity_id': datastore['id'],
    'task_type': 'flickr_import',
    'key': 'celery_task_id',
    'value': 'All images have been successfully imported.',
    'state':'done',
    'error': u'',
    'last_updated': datetime.now().isoformat(' '),
    'entity_type': 'resource'
  }
  update = ckan.call_action(
    'task_status_update',
    task_status
  )


def flickr_group_pool_import(context, url):
  group_url = url  # u"https://www.flickr.com/groups/abccanberra/pool/55001756@N05/" ### SHOULD BE PROVIDED BY USER  ###

  # Group lookup
  group = flickr.urls.lookupGroup(url=group_url)
  # log.info(group)

  # Harvesting images from the group if possible
  if group[u"stat"] == u"fail":
    group_not_found('ObjectNotFound', group[u"message"])
  else:
    # We need to get group info for dataset
    group_info = flickr.groups.getInfo(group_id=group[u"group"][u"id"])

    dataset = {
      u"group_id": group[u"group"][u"id"],
      u"name": group[u"group"][u"groupname"][u"_content"],
      u"path_alias": group_info[u"group"][u"path_alias"] if group_info[u"group"][u"path_alias"] else None,
      u"description": group_info[u"group"][u"description"][u"_content"]
    }

    # exits if datsset exists and iamges should be updated
    site_url = config.get('ckan.site_url')
    dataset, update, datastore = flickr_group_pool_create_dataset(context, dataset)

    # we need to set update parameter dataset already exists
    if update:
      text = "Dataset already exists. <a target='_blank' href='" + site_url + "/dataset/" + dataset[
      u"name"] + "'>Please visit</a> it."
      update = True
    else:
      text = "Dataset has been created. <a target='_blank' href='" + site_url + "/dataset/" + dataset[
      u"name"] + "'>Please visit</a> the dataset."
      update = False

    # sends tasks to background
    data = {'datastore': datastore}
    toolkit.get_action('celery_flickr_import')(context, data)

    return {
      'text': text,
      'update': update,
      'datastore': datastore['id'],
    }