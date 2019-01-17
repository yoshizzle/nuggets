from nuggets.app import app
from nuggets.config import _cfg, _cfgi

import os
import locale

app.static_folder = os.path.join(os.getcwd(), "static")
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

if __name__ == '__main__':
    app.run(host=_cfg('debug-host'), port=_cfgi('debug-port'), debug=False)
