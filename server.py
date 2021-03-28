from aiohttp import web
from pathlib import Path, PurePath
import shlex
import asyncio
import aiofiles
import logging
from subprocess import PIPE
import argparse


async def archivate(request):
    archive_hash = request.match_info.get('archive_hash', "Anonymous")
    if not Path(f'{photo_catalog_path}/{archive_hash}').exists():
        return web.HTTPNotFound(text='Sorry, this archive is not exist or was removed')
        
    process = await asyncio.subprocess.create_subprocess_exec(
        'zip', '-r9', '-', f'{archive_hash}', stdout=asyncio.subprocess.PIPE, cwd=photo_catalog_path)

    response = web.StreamResponse(
        status=200,
        headers={
            'Content-Disposition': f'attachment; filename={archive_hash}.zip'
        }
    )
    response.enable_chunked_encoding()
    await response.prepare(request)

    try:
        while True:
            attachment = await process.stdout.read(n=100*1000)
            logging.info('Sending archive chunk ...')
            await response.write(attachment)

            if process.stdout.at_eof():
                await response.write_eof()
                break

            await asyncio.sleep(delay_time)
    except asyncio.CancelledError:
        logging.error('Download was interrupted')
    finally:
        process.kill()
        await process.communicate()
    
    return response
        


async def handle_index_page(request):
    async with aiofiles.open('index.html', mode='r') as index_file:
        index_contents = await index_file.read()
    return web.Response(text=index_contents, content_type='text/html')


def createParser():
    parser = argparse.ArgumentParser(description='Download zip archive')
    parser.add_argument('-l', '--log', action='store_const', const=True, help='Logging enabled', default=False)
    parser.add_argument('-d', '--delay', help='Server response delay (max - 5sec)', default=0, type=int)
    parser.add_argument('-p', '--path', help='Path to photo catalog', default='test_photos')

    return parser


def main():
    global delay_time
    global photo_catalog_path
    parser = createParser()
    args = parser.parse_args()

    if args.log:
        logging.basicConfig(level = logging.INFO)
    else:
        logging.disable(logging.CRITICAL)

    if args.delay > 5:
        delay_time = 5
    else:
        delay_time = arg.delay

    photo_catalog_path = PurePath(args.path)

    app = web.Application()
    app.add_routes([
        web.get('/', handle_index_page),
        web.get('/archive/{archive_hash}/', archivate),
    ])
    web.run_app(app)


if __name__ == '__main__':
    main()
