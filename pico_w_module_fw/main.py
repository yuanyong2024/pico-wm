from machine import UART,Pin,I2C
import network
import socket
import time

led = Pin(16,Pin.OUT)
led.value(1)

timeout_count = 2
while timeout_count:
    print(f"timeout count {timeout_count} before setting up the Wi-Fi config")
    timeout_count-=1
    time.sleep(1)
    
print("\r\nWelcome to the setup process for picoduino, Please follow below three steps to control the onboard led via browser\r\n")
print('Please input your Wi-Fi name:')
wifi_name = input()
print(f'your Wi-Fi name is "{wifi_name}",now please input your Wi-Fi password')
password = input()
print(f'your Wi-Fi password is "{password}"')
print("well done, your picoduino now is trying to connect to your Wi-Fi network")




#connect to wifi router and return the ip
def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(wifi_name, password)
    retry_count = 10
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        #blink for 1s insted of delay 1s
        for i in range(5):
            led.value(0)
            time.sleep(0.1)
            led.value(1)
            time.sleep(0.1)
            
        retry_count-=1
        if retry_count==0:
            break
    
    if retry_count == 0:
        print("ooops, picoduino cannot connect to you Wi-Fi network, please check your Wi-Fi name and password and press reset button for a pretry.!!!!!!!!!!")
        while True:
            led.value(0)
            time.sleep(1)
            led.value(1)
            time.sleep(1)
        
    led.value(1)   
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    print("\r\nPlease copy the above ip address to browser and press enter(or return on MAC OS)")
    print("And have fun with thet LED on and off example -:)")
    return ip

  
def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection


  
#only turn on and off led in webpaage.  
def webpage(state):
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <form action="./lighton">
            <input type="submit" value="Light on" />
            </form>
            <form action="./lightoff">
            <input type="submit" value="Light off" />
            </form>
            <p>LED is {state}</p>
            </body>
            </html>
            """
    return str(html)
    
    
#start a web server    
def serve(connection):
    #Start a web server
    state = 'OFF'
    temperature = 0
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/lighton?':
            led.value(1)
            state = 'ON'
            print("LED is on now")
        elif request =='/lightoff?':
            led.value(0)
            state = 'OFF'
            print("LED is off now")
        client.send(webpage(state))
        client.close()
        
        
        
try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()
        



