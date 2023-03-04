# SMS Payment Gateway

## How it works
This is a simple payment gateway that uses text messages from android devices to keep track of payments received. Once a payment is made the received transaction message is forwarded to a server using the SMSSync Application. The server extracts all relevant information including `transactionId`, `amount`, `phone number` and `name` (optional)`. The information is then stored in the database with the validity status.

The user is required to be logged in and enter the transaction Id received through the message. The system then verifies the transaction Id to link the payment made by the user by a corresponding record in the database.

All messages that can not be verified are stored in the database for future references.


## How to Set Up in development environment.
> **Requirements** <br>
> - A valid Lipa Number for any of the listed providers (Airtel, Vodacom, Tigo) with the associated SIM Card.
> - A working android phone with SMS Sync App installed. Included in this repository with the associated SIM Card.
>
> The following steps are only for testing purposes

- Create virtual environment and install install requirements in the current directory with <br> 
`python3 -m venv virtual`. Make sure  `python-venv` is installed in your system
- Activate the virtual environment and install requirements with  `pip install -r requirements.txt`. 
- Define API_KEY for your backend in `.env` file. Multiple keys can be added separated by comma (,). Any random secured string is required.

- (Optional) Set up the database you wish to use in   `settings.py`. Check configuration of your database [here](https://docs.djangoproject.com/en/4.1/ref/databases/). The default database is sqllite for simplicity.
- Run your project in localhost with `python manage.py runserver`
- Switch on Mobile Hotspot on your android device and connect your computer in the network
- Get the IP Address assigned for your device. For Linux devices, run the command `ifconfig` and locate the ip address  in format `196.168.***.***`. For Windows run `ipconfig`.
- Open the Integrations Tab in SMSSync App and choose custom service.
- Fill integration details and Copy the Ip address into the url field as `http://<ip address>>:<<port>>/api/pay`.
- Change Method to POST and data format to JSON.
- Fill in the API_KEY generated into secret key field and change key for secret to 'api_key'
- Test integration to see if a message appears in the backend terminal.
- Enable Start SMS Sync service and Make transactions.

> **Note:**
> - SMSSync must be set as default SMS app
> - Beware that all text messages received in your phone will not be visible and will be forwarded to the server. Be sure that there are no important messages associated with the device.

## Seting up for production
In production environment, host your backend in a remote server and add the domain name of your server in the url field in SMSSync App. Make sure that the device has constant access to internet for sync to be successful.



## Database Schema
### CustomUser
| Field        | Description     |
|--------------|-----------|
|username | Username defined by user
|password | Password
|uuid | Unique User Identifier

> Includes default User fields defined by Django
### **Payments**  
| Field        | Description     | Nullable |
|--------------|-----------|------------|
| message |`str` Full text message received    | No       |
|   name | `str` Name extracted from the text message | Yes
|   sender    | `str` Sender of the text message (Provider)  | No     |
| number   | `str` Phone number of the customer extracted from the message | Yes
|transactiodId | `str` Transaction Id extracted from the message | No
|amount | `int` The amount received from the transaction | No
| is_valid |`bool` Validity of a transaction. If a transaction is verified then is valid becomes true | No
| valid_until| `timestamp` The date to which the payment is valid. Useful for subscription based services | Yes
| user | `int` The user associated with this transaction | No
| created |`timestamp` The date of creation of a given record | No

### InvalidPayments
| Field        | Description     | Nullable |
|--------------|-----------|------------|
| message |`str` Full text message received    | No       |
|   name | `str` Name extracted from the text message | Yes
|   sender    | `str` Sender of the text message (Provider)  | No     |
| number   | `str` Phone number of the customer extracted from the message | Yes
|transactiodId | `str` Transaction Id extracted from the message | Yes
|amount | `int` The amount received from the transaction | Yes
| reason |`str` Reason for the invalidity of the message | No
| created |`timestamp` The date of creation of a given record | No


## Contribution
The project is open to contributions and customization. This version gives the overview of how the gatewat works. Testing and improvements are appreciated.