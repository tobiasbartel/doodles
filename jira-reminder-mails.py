#!/usr/bin/env python

import smtplib
from email.mime.text import MIMEText

from jira.client import JIRA
from pprint import pprint as pp

options = {
    'server': 'http://ticket.ps-toys.de'
}

j = JIRA(options, basic_auth=('username', 'password'))

result = j.search_issues('project = "My Project" AND status = resolved AND resolved < -4d')

for issue in result:
    msg = MIMEText("Hello %s,\n\nyou are receiving this EMail because there is an issue at %s/browse/%s that needs to be reviewed by you.\nPlease go to %s/browse/%s and either close or reopen \"%s - %s\".\n\nKind regards,\n\nThe Team"  % (issue.fields.reporter.displayName, options['server'], issue.key, options['server'], issue.key, issue.key, issue.fields.summary))
    msg['Subject'] = 'Please review "%s" - %s ' % (issue.fields.summary, issue.key)
    msg['From'] = 'Web Operations Team <foo@bar.com>'
    msg['To'] = '%s <%s>' % (issue.fields.reporter.displayName, issue.fields.reporter.emailAddress)

    s = smtplib.SMTP('localhost')
    s.sendmail("foo@bar.com", issue.fields.reporter.emailAddress, msg.as_string())
    s.quit()
