from fastapi import FastAPI, APIRouter
from fastapi_socketio import SocketManager

sw = FastAPI()
app = FastAPI()
router = APIRouter()

sm = SocketManager(
    app=sw,
    mount_location = "", # default str : /ws
    socketio_path = "socket.io", # default str : socket.io
    cors_allowed_origins = '*' # default str or list : '*' or ['','']
)

@router.get('/')
async def index():...

app.include_router(router, prefix="/pro")

app.mount('/', sw)

@sm.on('notification') # nhận request từ dưới client
async def handle_status(sid, *args, **kwargs):
    arg = dict(*args)
    print (arg)
