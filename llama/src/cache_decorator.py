from functools import wraps
from flask import request, Response, current_app, jsonify
import hashlib
import json
from src.redis_provider import get_redis_client
# mongopy dependency

def generate_cache_key():
    request_data = f"{request.path}:{json.dumps(request.args)}"
    return hashlib.md5(request_data.encode('utf-8')).hexdigest()

def cache_response(timeout=60):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = generate_cache_key()
            redis_client = get_redis_client()

            if redis_client:
                try:
                    cached_response = redis_client.get(cache_key)
                    if cached_response:
                        current_app.logger.info(f"Cache hit for key: {cache_key}")
                        return Response(cached_response, mimetype='application/json')
                except Exception as e:
                    current_app.logger.error(f"Redis error: {str(e)}")
            else:
                current_app.logger.warning("Redis client is not available, proceeding without cache.")

            result = f(*args, **kwargs)

            # Ensure the response is a Response object
            if isinstance(result, tuple):
                if len(result) == 2:
                    response_data, status_code = result
                    response = Response(response_data, status=status_code, mimetype='application/json')
                elif len(result) == 3:
                    response_data, status_code, headers = result
                    response = Response(response_data, status=status_code, headers=headers, mimetype='application/json')
            elif isinstance(result, Response):
                response = result
            else:
                response = Response(json_util.dumps(result), mimetype='application/json')

            if redis_client:
                try:
                    if response.status_code == 200:
                        redis_client.setex(cache_key, timeout, response.get_data(as_text=True))
                        current_app.logger.info(f"Cache set for key: {cache_key}")
                except Exception as e:
                    current_app.logger.error(f"Redis error: {str(e)}")

            return response
        return decorated_function
    return decorator
