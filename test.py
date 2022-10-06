from jira import JIRA
import re

class Logowanie():

    def __init__(self, adres, mail, token):

        self.server_url = {'server': adres}
        self.auth_jira = JIRA(self.server_url, basic_auth=(mail, token))
        allfields = self.auth_jira.fields()
        self.nameMap = {self.auth_jira.field['name']:self.auth_jira.field['id'] for self.auth_jira.field in allfields}

    def take_csd_data(self, value_of_csd):

        for i in self.auth_jira.search_issues('status=pending AND project="Customer Service Desk" AND created > "2022/01/01"', maxResults=1000):
            if str(i.fields.issuetype) == 'RMA' and str(i.fields.status) == 'Pending' and str(i.key) == 'CSD-' + value_of_csd:
                return i.key, i.fields.summary, i.fields.components, i.fields.assignee, \
                       getattr(i.fields, self.nameMap["Quantity"]), i.fields.reporter,

    # def take_csd_data(self):
    #
    #     for i in self.auth_jira.search_issues('status=pending AND project="Customer Service Desk" AND created > "2022/01/01"', maxResults=1000):
    #         if str(i.fields.issuetype == 'RMA'):
    #             print(f'{i.key}, {i.fields.summary}')

# for projects in auth_jira.projects():
#     print(projects)
#
#
# # for issue in auth_jira.search_issues('assignee = currentUser()', maxResults=False):
# #     if str(issue.fields.issuetype) == 'RMA' and str(issue.fields.status) == 'Pending':
# #         print(issue)
#
# allfields = auth_jira.fields()
# nameMap = {auth_jira.field['name']:auth_jira.field['id'] for auth_jira.field in allfields}
#
# for i in auth_jira.search_issues(jql_str='project = "Customer Service Desk"', maxResults=100):
#     if str(i.fields.issuetype) == 'RMA' and str(i.fields.status) == 'Pending':
#         print(f'Numer: {i.key} temat sprawy: {i.fields.summary} komponent: '
#               f'{i.fields.components} przypisana do:  {i.fields.assignee} '
#               f'{getattr(i.fields, nameMap["Quantity"])}')

# if __name__ == '__main__':
#
#
    # print(a.take_csd_data('CSD-7753'))


    # test_str = "RMA/2023/06/12  siemanko1323ihczxbdka"
    #
    # a = re.findall("^0?(?:[1-30]|1[0-30])\/0?(?:[1-30]|1[0-30]|3[01])\/2\d{3}",test_str)
    #
    # print(a)
    #
    # b = re.search("^[a-zA-Z0-9]{3}[/.-](\d{4})[/.-](\d{2})[/.-](\d{2})", test_str)
    # print(b.group())

