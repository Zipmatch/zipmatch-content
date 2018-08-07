from flask import Blueprint, jsonify

from ..extensions import cache

blueprint = Blueprint('cache', __name__)


@blueprint.route('/clear')
def clear():
    cache.clear()
    return jsonify({})


@blueprint.route('/invalidate/<path:path>')
def delete_lead(path):
    cache_key = '/v1/content/{}'.format(path)
    cache.delete(cache_key)
    return jsonify({})
