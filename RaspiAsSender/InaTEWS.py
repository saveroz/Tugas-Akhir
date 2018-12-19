
import datetime 
import rockBlock
import time
from rockBlock import rockBlockProtocol
import serial


"""
NOTE:
All Credits go to Makersnake who make rockblock library in python     
Script ini dibuat untuk menerima data dari arduino
via serial usb di raspberry pi3 dan mengirimkan data tersebut melalui modul satelit 
ke thingspeak

"""
class Example (rockBlockProtocol):
    
        SLEEP_INTERVAL = 0.5 # delay interval pengiriman 
           
    def main(self):
        port="/dev/ttyACM0" # inialiasasi port arduino
    
        while(True):
            try:
                ser=serial.Serial(port,9600)
                data=ser.readline()
                data_split=data.split(",") # data dibagi menjadi 3 bagian 
                val1=data_split[0] 
                val2=data_split[1]
                val3=data_split[2]
            except serial.serialutil.SerialException: #deteksi error Serial
                print "port gak kedeteksi broo!!, coba ane ganti portnya dulu"
                if port=="/dev/ttyACM1": #ganti port ketika terjadi error
                    port="/dev/ttyACM0"
                elif port=="/dev/ttyACM0":
                    port="/dev/ttyACM1"
            except:
                print "unknown error tapi program tetap harus berjalan"
            else:
                try:
                    if val1!=None and val2!=None and val3!=None:
                        self.emit(val1,val2,val3)
                except: #ketika terjadi error
                    print "pengiriman error"
                else:
                    time.sleep(10) #delay ketika pengiriman berhasil
            finally:    
                time.sleep(self.SLEEP_INTERVAL)
            
                                
    def emit(self, val1,val2,val3):
            
        rb = rockBlock.rockBlock("/dev/ttyUSB0", self)
        
        rb.sendMessage(","+ str(val1)+","+str(val2)+","+str(val3)+","+"0"+","+"0"+","+"0")
                                                                                  
        rb.close()
    def rockBlockTxStarted(self):
        logA=datetime.datetime.now()
        print "rockBlockTxStarted"
        print logA
        
    def rockBlockTxFailed(self):
        logB=datetime.datetime.now()
        print "rockBlockTxFailed"
        print logB
        
    def rockBlockTxSuccess(self,momsn):
        logC=datetime.datetime.now()
        print "rockBlockTxSuccess " + str(momsn)
        print logC
        
if __name__=='__main__':
    Example().main()
      
