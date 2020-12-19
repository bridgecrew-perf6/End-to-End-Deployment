import scrapy
import json
from ..items import CompanyprofilescrawlItem


class CompanyProfilesSpider(scrapy.Spider):
    name = 'profiles'
    base_url = "https://www.idx.co.id/umbraco/Surface/ListedCompany/GetCompanyProfilesDetail?emitenType=&kodeEmiten="
    url = "https://www.idx.co.id/umbraco/Surface/Helper/GetEmiten?emitenType=s"

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse_code)

    def parse_code(self, response):
        response_code_to_json= json.loads(response.text, strict=False)
        code_list = [code['KodeEmiten'] for code in response_code_to_json]
        for each_unique_code in code_list[0:10]:
            url = self.base_url + each_unique_code
            yield scrapy.Request(url=url, callback=self.parse_data)

    def office_address(self,office_address_value):
        return office_address_value.replace('\r', '').replace('\n', ' ')

    def fax(self,fax_value):
        return [''.join('+62 '+fax) for fax in fax_value.split(',')]

    def sector(self,sector_value):
        return sector_value

    def sub_sector(self,sub_sector_value):
        return sub_sector_value

    def corporate_secretary(self, secr_data):
        if secr_data != []:
            secr_pop_list = ['Website', 'Fax', 'HP']
            secr_data = secr_data[0]
            for element in secr_pop_list:
                secr_data.pop(element, None)
            secr_data['name'] = secr_data.pop('Nama')
            secr_data['email'] = secr_data.pop('Email')
            secr_data['Phone'] = secr_data.pop('Telepon')

        return secr_data

    def director(self, direc_data):
        for element in direc_data:
            del element['Afiliasi']
            element['name'] = element.pop('Nama')
            element['position'] = element.pop('Jabatan')
            if element['position'] == '':
                element['position'] = 'Data is not available in the website'

        return direc_data

    def subsidiary(self, subs_data):
        secr_pop_list = ['Lokasi','MataUang','Satuan','StatusOperasi','TahunKomersil']
        for pair in subs_data:
            for key in secr_pop_list:
                pair.pop(key, None)
            pair['name'] = pair.pop('Nama')
            pair['type'] = pair.pop('BidangUsaha')
            pair['total asset'] = pair.pop('JumlahAset')
            pair['percentage'] = pair.pop('Persentase')

        return subs_data

    def parse_data(self, response):
        items = CompanyprofilescrawlItem()
        response_data_to_json = json.loads(response.text, strict=False)
        common_index = response_data_to_json['Profiles'][0]
        items["Company_Name"] = common_index['NamaEmiten']
        items["Security_Code"] = common_index['KodeEmiten']
        items["Office_address"] = self.office_address(common_index['Alamat'])
        items["Email"] = common_index['Email']
        items["Country"] = "Indonesia"
        items["Phone"] = '+62 '+common_index['Telepon']
        items["Fax"] = self.fax(common_index['Fax'])
        items["NPWP"] = common_index['NPWP']
        items["Company_Website"] = common_index['Website']
        items["IPO_Date"] = common_index['TanggalPencatatan'].split('T')[0]
        items["Board"] = common_index['PapanPencatatan'].upper()
        items["Sector"] = self.sector(common_index['Sektor'])
        items["Sub_Sector"] = self.sub_sector(common_index['SubSektor'])
        items["Registrar"] = common_index['BAE']
        items["Corporate_Secretary"] = self.corporate_secretary(response_data_to_json["Sekretaris"])
        items["Director"] = self.director(response_data_to_json["Direktur"])
        items["Subsidiary"] = self.subsidiary(response_data_to_json["AnakPerusahaan"])

        yield items


