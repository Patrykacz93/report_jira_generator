from jira import JIRA

class Logowanie():

    def __init__(self, adres, mail, token):

        self.server_url = {'server': adres}
        self.auth_jira = JIRA(self.server_url, basic_auth=(mail, token))
        allfields = self.auth_jira.fields()
        self.nameMap = {self.auth_jira.field['name']:self.auth_jira.field['id'] for self.auth_jira.field in allfields}

    def take_csd_data(self, value_of_csd):

        for i in self.auth_jira.search_issues('status=pending AND project="Customer Service Desk" AND created > "2022/01/01"', maxResults=1000):
            if str(i.fields.issuetype) == 'RMA' and str(i.fields.status) == 'Pending' and str(i.key) == "CSD-" + value_of_csd:
                return i.key, i.fields.summary, i.fields.components, i.fields.assignee, \
                       getattr(i.fields, self.nameMap["Quantity"]), i.fields.reporter, \
                       getattr(i.fields, self.nameMap["Serial Number"]), getattr(i.fields, self.nameMap["Organizations"])



