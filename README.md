# RealisticRaceCar
gameGUI.py、thread_joy.py、qrcode.py、request.py、csi_camera.py、Timer.py是主要會用到的。<br>
gameGUI.py是主要用來運行的城市，主要是GUI以及呼叫其他程式。
thread_joy.py只有在Linux有用，負責讀取搖桿及控制車輛。<br>
qrcode.py是用來解析影像中的qrcode。<br>
request.py負責跟伺服器溝通，以及呼叫伺服器API。<br>
csi_camera.py是一隻單獨讀取相機的影像的程式。<br>
Timer.py是負責紀錄時間，並回傳查核點時間的程式。<br>
其餘皆為測試用程式碼。<br>
