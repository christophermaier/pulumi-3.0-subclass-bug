Subclassed `Resource`s appear to behave differently between Pulumi 2.x
and 3.x. In particular, input properties on subclassed resources are
not available as implicit output properties.

The accompanying Pulumi stack creates an AWS DynamoDB table and an
item in that table. It then creates a Python subclass of
`pulumi_aws.dynamodb.Table` with the exact same properties as the
"raw" table created earlier. However, a
`pulumi_aws.dynamodb.TableItem` that depends on this table's
`hash_key` property cannot be created.

Additionally, input properties of the subclassed resource cannot be
exported as stack outputs.

The enclosed Makefile encapsulates running these two scenarios with
the `run-two` and `run-three` targets, which illustrate the behavior
with Pulumi 2.x libraries and 3.x libraries, respectively. The Pulumi
3.0 CLI was used in both cases.

```sh
make setup
```

```sh
❯ make run-two
pulumi destroy --yes
Previewing destroy (test):

Resources:

Destroying (test):

Resources:

Duration: 1s

The resources in the stack have been deleted, but the history and configuration associated with the stack are still maintained.
If you want to remove the stack completely, run 'pulumi stack rm test'.
rm -Rf venv
cp requirements-2.0.txt requirements.txt
pulumi up --yes
Previewing update (test):
     Type                       Name                          Plan
 +   pulumi:pulumi:Stack        pulumi-3.0-bug-testcase-test  create
 +   ├─ aws:dynamodb:Table      subclass-table                create
 +   ├─ aws:dynamodb:Table      raw-table                     create
 +   ├─ aws:dynamodb:TableItem  test-item-subclass            create
 +   └─ aws:dynamodb:TableItem  test-item                     create

Resources:
    + 5 to create

Updating (test):
     Type                       Name                          Status
 +   pulumi:pulumi:Stack        pulumi-3.0-bug-testcase-test  created
 +   ├─ aws:dynamodb:Table      subclass-table                created
 +   ├─ aws:dynamodb:Table      raw-table                     created
 +   ├─ aws:dynamodb:TableItem  test-item                     created
 +   └─ aws:dynamodb:TableItem  test-item-subclass            created

Outputs:
    raw_table_arn              : "arn:aws:dynamodb:<REGION>:<ACCOUNT_ID>:table/raw-table-cfb5c3b"
    raw_table_billing_mode     : "PAY_PER_REQUEST"
    raw_table_hash_key         : "x"
    raw_table_name             : "raw-table-cfb5c3b"
    subclass_table_arn         : "arn:aws:dynamodb:<REGION>:<ACCOUNT_ID>:table/subclass-table-1b00e98"
    subclass_table_billing_mode: "PAY_PER_REQUEST"
    subclass_table_hash_key    : "x"
    subclass_table_name        : "subclass-table-1b00e98"

Resources:
    + 5 created

Duration: 14s

pulumi stack
Current stack is test:
    Managed by penguin
    Last updated: 1 second ago (2021-04-21 13:52:23.345047721 -0400 EDT)
    Pulumi version: v3.0.0
Current stack resources (6):
    TYPE                                     NAME
    pulumi:pulumi:Stack                      pulumi-3.0-bug-testcase-test
    ├─ aws:dynamodb/table:Table              raw-table
    ├─ aws:dynamodb/tableItem:TableItem      test-item
    ├─ aws:dynamodb/table:Table              subclass-table
    ├─ aws:dynamodb/tableItem:TableItem      test-item-subclass
    └─ pulumi:providers:aws                  default_3_38_1

Current stack outputs (8):
    OUTPUT                       VALUE
    raw_table_arn                arn:aws:dynamodb:<REGION>:<ACCOUNT_ID>:table/raw-table-cfb5c3b
    raw_table_billing_mode       PAY_PER_REQUEST
    raw_table_hash_key           x
    raw_table_name               raw-table-cfb5c3b
    subclass_table_arn           arn:aws:dynamodb:<REGION>:<ACCOUNT_ID>:table/subclass-table-1b00e98
    subclass_table_billing_mode  PAY_PER_REQUEST
    subclass_table_hash_key      x
    subclass_table_name          subclass-table-1b00e98

Use `pulumi stack select` to change stack; `pulumi stack ls` lists known ones
```

Here, we see that output and input properties are available on both
the raw `dynamodb.Table` resource, as well as the subclassed resource.

Also, note that the `hash_key` and `billing_mode` properties of the
subclassed table show up in the stack outputs.

With the 3.0 dependencies, however, this fails.

```sh
make run-three
pulumi destroy --yes
Previewing destroy (test):

Resources:

Destroying (test):

Resources:

Duration: 1s

The resources in the stack have been deleted, but the history and configuration associated with the stack are still maintained.
If you want to remove the stack completely, run 'pulumi stack rm test'.
rm -Rf venv
cp requirements-3.0.txt requirements.txt
pulumi up --yes
Previewing update (test):
     Type                       Name                          Plan
 +   pulumi:pulumi:Stack        pulumi-3.0-bug-testcase-test  create
 +   ├─ aws:dynamodb:Table      subclass-table                create
 +   ├─ aws:dynamodb:Table      raw-table                     create
 +   ├─ aws:dynamodb:TableItem  test-item-subclass            create
 +   └─ aws:dynamodb:TableItem  test-item                     create

Resources:
    + 5 to create

Updating (test):
     Type                       Name                          Status         Info
 +   pulumi:pulumi:Stack        pulumi-3.0-bug-testcase-test  created
 +   ├─ aws:dynamodb:Table      subclass-table                created
 +   ├─ aws:dynamodb:Table      raw-table                     created
 +   ├─ aws:dynamodb:TableItem  test-item                     created
     └─ aws:dynamodb:TableItem  test-item-subclass            **failed**     1 error

Diagnostics:
  aws:dynamodb:TableItem (test-item-subclass):
    error: aws:dynamodb/tableItem:TableItem resource 'test-item-subclass' has a problem: Missing required argument: The argument "hash_key" is required, but no definition was found.. Examine values at 'TableItem.HashKey'.

Outputs:
    raw_table_arn         : "arn:aws:dynamodb:<REGION>:<ACCOUNT_ID>:table/raw-table-59a48e6"
    raw_table_billing_mode: "PAY_PER_REQUEST"
    raw_table_hash_key    : "x"
    raw_table_name        : "raw-table-59a48e6"
    subclass_table_arn    : "arn:aws:dynamodb:<REGION>:<ACCOUNT_ID>:table/subclass-table-154c689"
    subclass_table_name   : "subclass-table-154c689"

Resources:
    + 4 created

Duration: 14s

make: *** [Makefile:20: run-three] Error 255
```

Note that a `dynamodb.TableItem` could not be produced because the
`hash_key` property of the subclassed table was not available.

Similarly, the `hash_key` and `billing_mode` properties of the
subclassed table do not appear as stack outputs.


To clean up, run:

```sh
make destroy
```
