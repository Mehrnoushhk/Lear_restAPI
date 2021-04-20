import uvicorn
from fastapi import FastAPI, Response, status

api = FastAPI()

items = []


@api.get('/item/{item_name}', status_code=200)
async def get_item(item_name, response: Response):
    for item in items:
        if item['name'] == item_name:
            return item
    response.status_code = status.HTTP_404_NOT_FOUND
    return {'item': None}


@api.post('/item/{item_name}')
async def create_item(item_name):
    item = {
        'name': item_name,
        'price': 100.0 
    }
    items.append(item)
    return item


if __name__ == '__main__':
    uvicorn.run('main:api', reload=True)