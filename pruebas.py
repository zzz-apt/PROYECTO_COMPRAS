from seleniumbase import Driver
from seleniumbase import SB
import time 

os_binary_location = "/usr/bin/chromium"

driver = Driver(
    undetectable=None,     
    uc=None,               
    block_images=True,
    window_size='1920,1080',  
    headless1=True,  
    chromium_arg=None, 
    binary_location=os_binary_location, 
    disable_csp=True,       
    incognito=True,       
    mobile=False,
    pls='none',
    driver_version="system"   # ("system" en Linux, "keep" en Windows)
)


driver.get("https://www30.mercantilbanco.com/login")

print('entrando a pagina')

# Cambiar el User Agent para la siguiente petición PUEDE QUE AYUDE A MEJORAR LAS COMPRAS

time.sleep(20)
driver.save_screenshot('ERROR.png')

