import asyncio
import json
from aiohttp import web
import aiohttp_jinja2
import jinja2
import os

async def start_web_server(kartr):
    app = web.Application()
    app['kartr'] = kartr

    current_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(current_dir, 'templates')
    
    os.makedirs(template_dir, exist_ok=True)

    aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(template_dir))

    app.router.add_get('/', handle_index)
    app.router.add_post('/command', handle_command)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 0)
    await site.start()
    
    for sock in site._server.sockets:
        port = sock.getsockname()[1]
        return f'http://localhost:{port}'

async def handle_index(request):
    return aiohttp_jinja2.render_template('index.html', request, {})

async def handle_command(request):
    try:
        data = await request.json()
        command = data['command']
        result = await request.app['kartr'].process_command(command)
        return web.json_response({'result': result})
    except json.JSONDecodeError:
        return web.json_response({'error': 'Invalid JSON'}, status=400)
    except KeyError:
        return web.json_response({'error': 'Missing command'}, status=400)
    except Exception as e:
        return web.json_response({'error': str(e)}, status=500)
