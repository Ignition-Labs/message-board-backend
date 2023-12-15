import random
from db import op
from web3 import Web3
import logging

logger = logging.getLogger(__name__)


def verify_address_and_convert(address: str):
    try:
        address = Web3.to_checksum_address(address)
        return address
    except:
        return None


def verify_code(code: str):
    if type(code) == str and len(code) == 6:
        for char in code:
            try:
                int(char)
            except:
                return False
        return True
    else:
        return False


def get_user_msg(code: str, address: str):
    return op.query_msg_by_address_and_code(code=code, address=address)


def get_user_content(code: str, address: str):
    return op.qeury_mappings_by_code(code=code, address=address)


def update_content(code: str, address: str, content: str):
    op.update_content(code, address, content)


def update_region(code: str, address: str, region: str):
    op.update_region(code, address, region)


def update_name(code: str, address: str, name: str):
    op.update_name(code, address, name)


def update_avatar(code: str, address: str, avatar: str):
    op.update_avatar(code, address, avatar)





















############################ ADMIN ################################

def gen_new_code():
    new_code = ""
    for i in range(6):
        new_code += str(random.randint(0, 9))
    op.add_msg(code = new_code, region="TaiWan")
    return new_code


def gen_many_new_code(many: int):
    codes = []
    for i in range(many):
        codes.append(gen_new_code())
    return codes


def gen_many_new_code(many: int):
    codes = []
    for i in range(many):
        codes.append(gen_new_code())
    return codes


def connect_all():
    codes = op.all_codes()
    for code in codes:
        print("code: " + code)
        codes_connected = op.random_choose_mapping(code)
        print(f"code: {code}, conn: {codes_connected}")
        op.add_many_random_mapping(code=code, codes_connected=codes_connected)        
    


def judge():
    data = [
        "821100",
        "896148",
        "416797",
        "366137",
        "979229",
        "135554",
        "424144",
        "584844",
        "719882",
        "020456",
        "907376",
        "313887",
        "363864",
        "881395",
        "664742",
        "048804",
        "622227",
        "028534",
        "748146",
        "773972",
        "516262",
        "662695",
        "938367",
        "936421",
        "740049",
        "576386",
        "737508",
        "266874",
        "211396",
        "791447",
        "076997",
        "658445",
        "972592",
        "992714",
        "233698",
        "065382",
        "079703",
        "053914",
        "829417",
        "263464",
        "097601",
        "761683",
        "655070",
        "335120",
        "435027",
        "410917",
        "389410",
        "901022",
        "830108",
        "875083",
        "772062",
        "156374",
        "724284",
        "884174",
        "952801",
        "691317",
        "559826",
        "175526",
        "137019",
        "292525",
        "588559",
        "816578",
        "497709",
        "793469",
        "964710",
        "999933",
        "486505",
        "708522",
        "142430",
        "283032",
        "981107",
        "184483",
        "222966",
        "309932",
        "907085",
        "038091",
        "735214",
        "616650",
        "306330",
        "877078",
        "074444",
        "159021",
        "070214",
        "317369",
        "349140",
        "981252",
        "603457",
        "807894",
        "511126",
        "561848",
        "724066",
        "140458",
        "983717",
        "594206",
        "148667",
        "193997",
        "051286",
        "484101",
        "630049",
        "721431",
        "724289",
        "587666",
        "316638",
        "506625",
        "863987",
        "236737",
        "459560",
        "485003",
        "487310",
        "321042",
        "645161",
        "995104",
        "222479",
        "286116",
        "653610",
        "312495",
        "560689",
        "494975",
        "058533",
        "643796",
        "906840",
        "283575",
        "756448",
        "712789",
        "258628",
        "063012",
        "041140",
        "553358",
        "256400",
        "234173",
        "212070",
        "903854",
        "825982",
        "779951",
        "259246",
        "080264",
        "703716",
        "488405",
        "346896",
        "919623",
        "416927",
        "979341",
        "341464",
        "979833",
        "680165",
        "158174",
        "520552",
        "183832",
        "940255",
        "360652"
    ]
    # 利用集合来找出重复值
    duplicates = set()
    unique_items = set()

    for item in data:
        if item in unique_items:
            duplicates.add(item)
        else:
            unique_items.add(item)

    if duplicates:
        print("重复值:", duplicates)
    else:
        print("没有重复值")