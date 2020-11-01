# Text Service Application
## About Application
Application operates on two modes:
 - Change text: The sender sends the text file to the server and the json file, in respond the server must read the json file and swap the words from the text according the json file.
 - Encode/Decodetext: The sender sends the text file and the key (another text) to the server, on the respond the server must XOR the text message with the key (One Time Pad cipher) and return it to the client. The decoding process happens in the same way where instead of the text message the client sends the encrypted text.
 
 ## Installation
 - Application can be installed using following command from console:
 ```sh
  git clone https://github.com/xeyal-ferzelibeyli/text_service.git
 ```
 - To install all the required packages:
  ```sh
  pip install requirements.txt
 ```
 
 ## Usage
  - First you open two console window one for server, another for client. For server:
   ```sh
  python3 text_service.py server -p <port_number>
   ```
   For client:
   ```sh
  python3 text_service.py client --host <ip_address> -p <port_number> --mode <mode> --msg_file <file_path> --aux_file <file_path>
   ```
   Here --aux_file option can be either key or json file according to specified mode. 
