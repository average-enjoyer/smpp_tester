import logging
import sys

import smpplib.gsm
import smpplib.client
import smpplib.consts

# if you want to know what's happening
logging.basicConfig(level='DEBUG')

# Two parts, UCS2, SMS with UDH
parts, encoding_flag, msg_type_flag = smpplib.gsm.make_parts(u'Sup dude!')

client = smpplib.client.Client('192.168.0.170', 2775, allow_unknown_opt_params=True)

# Print when obtain message_id
client.set_message_sent_handler(
    lambda pdu: sys.stdout.write('sent {} {}\n'.format(pdu.sequence, pdu.message_id)))
client.set_message_received_handler(
    lambda pdu: sys.stdout.write('delivered {}\n'.format(pdu.receipted_message_id)))

client.connect()
client.bind_transceiver(system_id='login', password='secret')

for part in parts:
    pdu = client.send_message(
        source_addr_ton=smpplib.consts.SMPP_TON_INTL,
        # source_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
        # Make sure it is a byte string, not unicode:
        source_addr='777000',

        dest_addr_ton=smpplib.consts.SMPP_TON_INTL,
        # dest_addr_npi=smpplib.consts.SMPP_NPI_ISDN,
        # Make sure thease two params are byte strings, not unicode:
        destination_addr='123002',
        short_message=part,

        data_coding=encoding_flag,
        esm_class=msg_type_flag,
        registered_delivery=True,
    )
    print(pdu.sequence)

# Enters a loop, waiting for incoming PDUs
client.listen()
