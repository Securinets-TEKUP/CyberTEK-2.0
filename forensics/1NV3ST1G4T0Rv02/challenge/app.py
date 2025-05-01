#!/usr/bin/env python3

correct_answers = {

"The spy is using patterns to secure the system, unlock the phone !": "12569",
"The spy had our secret base location, he didn't say how he received it !\\ recover the broken file and get the GPS location ! flag format: GPS_Coo": "-51.50310107537177_-58.994881776473875",
"It's impossible that he has identified our location alone ! Who told him ?": "Roberta Aizenberg",
"Identify how many SIM the SPY has and which Service Provider is compromised! : flag format : number_provider ": "2_Movistar",
" where did he meet his Handler? flag format: geolocation,name":" -51.79561607045942,-58.94036530322086,Argentine Military Cemetery",
"The handler is smart, find the hidden message that the spy detects each time he recieves a call ?":"USE_The_Secret_APP",
"What is the md5 of the malicious APP":"db01f96d5e66d82f7eb61b85eb96ef6e",
"what is the name of the malware":"dendroid",
"what is the category of such malicious app":"Trojan",
"when it was firstly submitted in the community as malware":"2013-12-20 21:13:14 UTC",
"what are the top 7 malicious permissions of the app \\ flag format act1.act2.act3":"ACCESS_FINE_LOCATION.SEND_SMS.READ_CONTACTS.WRITE_SMS.PROCESS_OUTGOING_CALLS.WAKE_LOCK.GET_TASKS",
"The application is shared on a famous forum \\ what is the id of the sample and the forum name \\ flag format: Forum.domain_sample.id":"virus.exchange_4496147",
"let's dive deeper into analysis! What's the serial number of the RSA signature for this APK":"0x52802812",
"The malware communicates with Android's internal telephony service. What is the full name of the AIDL interface used to perform remote call control?":"com.android.internal.telephony.ITelephony",
"There is a method used in the application to show advanced surveillance and specific locations! name it":"getNeighboringCellInfo",
"What Hidden permission is required to use ITelephony interface":"android.permission.MODIFY_PHONE_STATE",
"The malicious application is communicating with a C2 server what interface is used to communicate with the remote server":"org.apache.http.client.HttpClient",
"What encoding method is used to hide the C2 URL before it is stored?":"base64",
"What unique identifier of the victim device is appended to the C2 request":"AndroidID",
"What remote command enables or disables call recording":"recordcalls",
"What remote command allows the attacker to block incoming SMS?":"blocksms",
"what is the url and the password of the C2 servser":"http://pizzachip.com/rat_keylimepie",
}

user_answers = {}

print("== 1NV3ST1G4T0R v.02 ==\n== by cybereagle2001 ==\nAnswer The questions save the Nation:\n")

for question in correct_answers:
    user_answers[question] = input(f"{question}\n> ")

if user_answers == correct_answers:
    print("Good job! \nFlag: Securinets{M0B1L3_1s_S0_1NTr3s3T1NG!}")
else:
    print("Sorry, incorrect answers.")
