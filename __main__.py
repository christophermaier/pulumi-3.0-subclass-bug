import pulumi
from pulumi_aws import dynamodb

raw_table = dynamodb.Table(
    "raw-table",
    attributes=[
        dynamodb.TableAttributeArgs(name="x", type="S")
    ],
    billing_mode="PAY_PER_REQUEST",
    hash_key="x"
)

pulumi.export("raw_table_name", raw_table.name)
pulumi.export("raw_table_arn", raw_table.arn) # Explicit output property
 # Input properties act as implicit output properties
pulumi.export("raw_table_hash_key", raw_table.hash_key)
pulumi.export("raw_table_billing_mode", raw_table.billing_mode)

item = dynamodb.TableItem(
    "test-item",
    table_name=raw_table.name,
    hash_key=raw_table.hash_key, # <-- implicit output property
    item='{"x": {"S": "hello world"}}'
)

# Everything above works fine.

########################################################################

class DynamoDBTableSubclass(dynamodb.Table):
    """
    Subclass of existing Table resource that creates the same kind of table as above.
    """
    def __init__(
        self,
        name: str,
    ) -> None:
        super().__init__(
            name,
            attributes=[
                dynamodb.TableAttributeArgs(name="x", type="S")
            ],
            billing_mode="PAY_PER_REQUEST",
            hash_key="x"
        )

subclass_table = DynamoDBTableSubclass("subclass-table")

pulumi.export("subclass_table_name", subclass_table.name)
# Explicit output property; still available
pulumi.export("subclass_table_arn", subclass_table.arn)
# Input properties; no longer available as an implicit output property
# with Pulumi 3.0.0
#
# This worked all through the 2.x line.
pulumi.export("subclass_table_hash_key", subclass_table.hash_key)
pulumi.export("subclass_table_billing_mode", subclass_table.billing_mode)

item = dynamodb.TableItem(
    "test-item-subclass",
    table_name=subclass_table.name,
    hash_key=subclass_table.hash_key, # <-- not available in Pulumi 3
    item='{"x": {"S": "hello world"}}'
)
