#!/usr/bin/env python3

############################################################################
#
# MODULE:       t.stac.item
# AUTHOR:       Corey T. White, OpenPlains Inc.
# PURPOSE:      Get items from a STAC API server
# COPYRIGHT:    (C) 2023-2024 Corey White
#               This program is free software under the GNU General
#               Public License (>=v2). Read the file COPYING that
#               comes with GRASS for details.
#
#############################################################################

# %module
# % description: Downloads and imports data from a STAC API server.
# % keyword: raster
# % keyword: import
# % keyword: STAC
# % keyword: temporal
# %end

# %option
# % key: url
# % type: string
# % description: STAC API Client URL
# % required: yes
# %end

# %option
# % key: collection_id
# % type: string
# % required: yes
# % multiple: no
# % description: Collection Id.
# %end

# %option
# % key: request_method
# % type: string
# % required: no
# % multiple: no
# % options: GET,POST
# % answer: POST
# % description:  The HTTP method to use when making a request to the service.
# % guisection: Request
# %end

# %option G_OPT_F_INPUT
# % key: settings
# % label: Full path to settings file (user, password)
# % description: '-' for standard input
# % guisection: Request
# % required: no
# %end

# %option
# % key: max_items
# % type: integer
# % description: The maximum number of items to return from the search, even if there are more matching results.
# % multiple: no
# % required: no
# % answer: 1000
# % guisection: Request
# %end

# %option
# % key: limit
# % type: integer
# % description: A recommendation to the service as to the number of items to return per page of results. Defaults to 100.
# % multiple: no
# % required: no
# % answer: 100
# % guisection: Request
# %end

# %option
# % key: ids
# % type: string
# % description: List of one or more Item ids to filter on.
# % multiple: no
# % required: no
# % guisection: Query
# %end

# %option
# % key: bbox
# % type: double
# % required: no
# % multiple: yes
# % description: The bounding box of the request in WGS84 (example [-72.5,40.5,-72,41]). (default is current region)
# % guisection: Query
# %end

# %option G_OPT_V_INPUT
# % key: intersects
# % required: no
# % description: Results filtered to only those intersecting the geometry.
# % guisection: Query
# %end

# %option
# % key: datetime
# % label: Datetime Filter
# % description: Either a single datetime or datetime range used to filter results.
# % required: no
# % guisection: Query
# %end

# %option
# % key: query
# % description: List or JSON of query parameters as per the STAC API query extension.
# % required: no
# % guisection: Query
# %end

# %option
# % key: filter
# % description: JSON of query parameters as per the STAC API filter extension
# % required: no
# % guisection: Query
# %end

# %option
# % key: asset_keys
# % label: Asset Keys
# % type: string
# % required: no
# % multiple: yes
# % description: List of one or more asset keys to filter item downloads.
# % guisection: Query
# %end

# %option
# % key: item_roles
# % label: Item roles
# % type: string
# % required: no
# % multiple: yes
# % description: List of one or more item roles to filter by.
# % guisection: Query
# %end

# %option
# % key: filter_lang
# % type: string
# % required: no
# % multiple: no
# % options: cql2-json,cql2-text
# % description: Language variant used in the filter body. If filter is a dictionary or not provided, defaults to cql2-json. If filter is a string, defaults to cql2-text.
# % guisection: Query
# %end

# %option
# % key: sortby
# % description: A single field or list of fields to sort the response by
# % required: no
# % guisection: Query
# %end

# %option
# % key: format
# % type: string
# % required: no
# % multiple: no
# % options: json,plain
# % description: Output format
# % guisection: Output
# % answer: json
# %end

# %option G_OPT_F_OUTPUT
# % key: strds_output
# % label: STRDS Output
# % description: Spatial Temporal Raster Dataset Registration File
# % guisection: Output
# % required: no
# %end

# %option
# % key: items_vector
# % type: string
# % description: Name of vector containing STAC item boundaries and metadata.
# % required: no
# % multiple: no
# % guisection: Output
# %end

# %option
# % key: method
# % type: string
# % required: no
# % multiple: no
# % options: nearest,bilinear,bicubic,lanczos,bilinear_f,bicubic_f,lanczos_f
# % description: Resampling method to use for reprojection (required if location projection not longlat)
# % descriptions: nearest;nearest neighbor;bilinear;bilinear interpolation;bicubic;bicubic interpolation;lanczos;lanczos filter;bilinear_f;bilinear interpolation with fallback;bicubic_f;bicubic interpolation with fallback;lanczos_f;lanczos filter with fallback
# % guisection: Output
# % answer: nearest
# %end

# %option
# % key: resolution
# % type: string
# % required: no
# % multiple: no
# % options: estimated,value,region
# % description: Resolution of output raster map (default: estimated)
# % descriptions: estimated;estimated resolution;value; user-specified resolution;region;current region resolution
# % guisection: Output
# % answer: estimated
# %end

# %option
# % key: resolution_value
# % type: double
# % required: no
# % multiple: no
# % description: Resolution of output raster map (use with option resolution=value)
# % guisection: Output
# %end

# %option
# % key: extent
# % type: string
# % required: no
# % multiple: no
# % options: input,region
# % description: Output raster map extent
# % descriptions: input;extent of input map;region; extent of current region
# % guisection: Output
# % answer: input
# %end

# %flag
# % key: m
# % description: Collection Search Item Summary
# %end

# %flag
# % key: i
# % description: Item metadata
# %end

# %flag
# % key: a
# % description: Asset metadata
# %end

# %flag
# % key: d
# % description: Dowload and import assets
# %end

# %flag
# % key: p
# % description: Pretty print the JSON output
# %end

# %option G_OPT_M_NPROCS
# %end

# %option G_OPT_MEMORYMB
# %end

import os
import sys
from pprint import pprint
import json
import gettext
from contextlib import contextmanager
import grass.script as gs
from grass.pygrass.utils import get_lib_path

# Set up translation function
_ = gettext.gettext


@contextmanager
def add_sys_path(new_path):
    """Add a path to sys.path and remove it when done"""
    original_sys_path = sys.path[:]
    sys.path.append(new_path)
    try:
        yield
    finally:
        sys.path = original_sys_path


def collect_item_assets(item, asset_keys, asset_roles):
    """
    Collect and return a list of asset dictionaries from a STAC item, filtered by asset keys and roles.

    :param item: STAC item object with 'assets', 'collection_id', 'id', and 'properties' attributes.
    :type item: object
    :param asset_keys: Asset keys to include. If None or empty, all asset keys are considered.
    :type asset_keys: list or set
    :param asset_roles: Asset roles to include. If None or empty, all asset roles are considered.
    :type asset_roles: list or set

    :return: List of asset dictionaries matching the provided keys and roles. Each dictionary includes 'collection_id', 'item_id', 'file_name', and 'datetime'.
    :rtype: list
    """
    requested_assets = []
    for key, asset in item.assets.items():
        asset_file_name = f"{item.collection_id}.{item.id}.{key}"
        # Check if the asset key is in the list of asset keys
        if asset_keys and key not in asset_keys:
            continue

        # Check if the asset fits the roles
        if asset_roles and not set(asset.roles) & set(asset_roles):
            continue

        asset_dict = asset.to_dict()
        # The output file name
        asset_dict["collection_id"] = item.collection_id
        asset_dict["item_id"] = item.id
        asset_dict["file_name"] = asset_file_name
        asset_dict["datetime"] = item.properties["datetime"]
        requested_assets.append(asset_dict)

    return requested_assets


def main():
    """Main function"""
    # Import dependencies
    path = get_lib_path(modname="t.stac", libname="staclib")
    if path is None:
        gs.fatal("Not able to find the stac library directory.")

    with add_sys_path(path):
        try:
            import staclib as libstac
        except ImportError as err:
            gs.fatal(f"Unable to import staclib: {err}")

    # STAC Client options
    client_url = options["url"]  # required
    collection_id = options["collection_id"]  # required

    # Request options
    limit = int(options["limit"])  # optional
    max_items = int(options["max_items"]) if options["max_items"] else None  # optional
    request_method = options["request_method"]  # optional

    # Query options
    bbox = options["bbox"]  # optional
    datetime = options["datetime"]  # optional
    query = options["query"]  # optional
    filter = options["filter"]  # optional
    filter_lang = options["filter_lang"]  # optional
    intersects = options["intersects"]  # optional
    # Asset options
    asset_keys_input = options["asset_keys"]  # optional
    asset_keys = asset_keys_input.split(",") if asset_keys_input else None

    item_roles_input = options["item_roles"]  # optional
    item_roles = item_roles_input.split(",") if item_roles_input else None

    # Flags
    summary_metadata = flags["m"]
    item_metadata = flags["i"]
    asset_metadata = flags["a"]
    download = flags["d"]
    pretty_print = flags["p"]  # optional

    # Output options
    strds_output = options["strds_output"]  # optional
    items_vector = options["items_vector"]  # optional
    method = options["method"]  # optional
    resolution = options["resolution"]  # optional
    resolution_value = options["resolution_value"]  # optional
    extent = options["extent"]  # optional
    format = options["format"]  # optional

    # GRASS import options
    method = options["method"]  # optional
    memory = int(options["memory"])  # optional
    nprocs = int(options["nprocs"])  # optional

    search_params = {}  # Store STAC API search parameters
    collection_items_assets = []

    # Set the request headers
    settings = options["settings"]
    req_headers = libstac.set_request_headers(settings)

    # Connect to STAC API
    stac_helper = libstac.STACHelper()
    stac_helper.connect_to_stac(client_url, req_headers)
    collection = stac_helper.get_collection(collection_id)

    if summary_metadata:
        if format == "plain":
            return libstac.collection_metadata(collection)
        elif format == "json":
            libstac.print_json_to_stdout(collection, pretty_print)

    # Start item search
    intersects_geojson = stac_helper.wgs84_geojson_from_vector(intersects)
    if intersects_geojson:
        search_params["intersects"] = intersects_geojson

    if options["ids"]:
        ids = options["ids"]  # item ids optional
        search_params["ids"] = ids.split(",")

    # Set the bbox to the current region if the user did not specify the bbox or intersects option
    if not bbox and not intersects_geojson:
        gs.verbose(_("Setting bbox to current region: {}").format(bbox))
        bbox = libstac.region_to_wgs84_decimal_degrees_bbox()
        search_params["bbox"] = bbox

    if datetime:
        search_params["datetime"] = datetime

    # Add filter to search_params
    # https://github.com/stac-api-extensions/filter
    if filter:
        if isinstance(filter, str):
            filter = json.loads(filter)
        if isinstance(filter, dict):
            search_params["filter"] = filter

    if filter_lang:
        search_params["filter_lang"] = filter_lang

    # TODO: Make this a fucntion and improve the code
    if query:
        if isinstance(query, str):
            try:
                query = json.loads(query)
            except json.JSONDecodeError as e:
                gs.fatal(f"Invalid JSON format for query: {e}")
        if isinstance(query, dict):
            search_params["query"] = query
        if isinstance(query, list):
            search_params["query"] = query

    # Add search parameters to search_params
    search_params["method"] = request_method
    search_params["collections"] = collection_id
    search_params["limit"] = limit
    search_params["max_items"] = max_items

    # Search the STAC API
    items_search = stac_helper.search_api(**search_params)

    # Create vector layer of items metadata
    if items_vector:
        libstac.create_vector_from_feature_collection(
            items_vector, items_search, limit, max_items
        )

    # Fetch items from all pages
    items = libstac.fetch_items_with_pagination(items_search, limit, max_items)

    # Report item metadata
    if item_metadata:
        if format == "plain":
            gs.message(_("bbox: {}\n").format(bbox))
            gs.message(_("Items Found: {}").format(len(list(items))))
            for item in items:
                stac_helper.report_stac_item(item)
            return None
        if format == "json":
            item_list = [item.to_dict() for item in items]
            libstac.print_json_to_stdout(item_list, pretty_print)
            return 0

    # Collect requested assets from each item
    for item in items:
        collection_items_assets.extend(
            collect_item_assets(item, asset_keys, asset_roles=item_roles)
        )

    if strds_output:
        strds_output = os.path.abspath(strds_output)
        libstac.register_strds_from_items(collection_items_assets, strds_output)

    if asset_metadata:
        if format == "plain":
            gs.message(
                _("%s Assets Ready for download...") % len(collection_items_assets)
            )
            for asset in collection_items_assets:
                libstac.report_plain_asset_summary(asset)
            return 0

        if format == "json":
            libstac.print_json_to_stdout(collection_items_assets, pretty_print)
            return 0

    if not summary_metadata and not item_metadata and not asset_metadata:
        estimate_download = libstac.estimate_download_size(collection_items_assets)
        if format == "json":
            libstac.print_json_to_stdout(estimate_download, pretty_print)

        if format == "plain":
            sys.stdout.write(f"Total Assests: {estimate_download['count']}\n")
            sys.stdout.write(
                f"Estimated download size: {estimate_download.get('bytes', 0) / 1e9} GB\n"
            )

    if download:
        # Download and Import assets
        libstac.download_assets(
            assets=collection_items_assets,
            resample_method=method,
            resample_extent=extent,
            resolution=resolution,
            resolution_value=resolution_value,
            memory=memory,
            nprocs=nprocs,
        )

    return 0


if __name__ == "__main__":
    options, flags = gs.parser()
    sys.exit(main())
