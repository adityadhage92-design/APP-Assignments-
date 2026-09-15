import re

EMAIL_PATTERN = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.-]+'


def find_emails(text):
    return re.findall(EMAIL_PATTERN, text)


def is_valid_email(candidate):
    return re.fullmatch(EMAIL_PATTERN, candidate) is not None


sample_text = """
Contact us at support@examplecorp.com.
You can also email sales.team@business-hub.co.in.
Rahul's email is rahul_23@gmail.com.
For promotions use newsletter+promo@my-site.org.
"""

emails = find_emails(sample_text)

print("Emails found:")
for email in emails:
    print(email)

print("Total emails found:", len(emails))

test_emails = [
    "user@site.com",
    "@missing-local.com",
    "plain.text@",
    "user@site",
    "a.b-c_d+e@sub.domain.co.in"
]

print("\nEmail Validation:")

for email in test_emails:
    if is_valid_email(email):
        print(email, "-> VALID")
    else:
        print(email, "-> INVALID")
