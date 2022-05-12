INFRASTRUCTURE_VERSION=terraform   #options: terraform / bicep / arm
CICD_AGENT=azure_devops   #options: azure_devops or github_actions
MLOPS_VERSION=aml-cli-v2   #options: aml-python-sdk / aml-cli-v2

if [ "$MLOPS_VERSION" != "aml-cli-v2" ] && [ "$MLOPS_VERSION" != "aml-python-sdk" ]
then
    echo "Wrong MLOPS_VERSION: $MLOPS_VERSION"
    exit 1
fi

if [ "$CICD_AGENT" != "azure_devops" ] && [ "$CICD_AGENT" != "github_actions" ]
then
    echo "Wrong CICD_AGENT: $CICD_AGENT"
    exit 1
fi

if [ "$INFRASTRUCTURE_VERSION" != "terraform" ] && [ "$INFRASTRUCTURE_VERSION" != "bicep" ] && [ "$INFRASTRUCTURE_VERSION" != "arm" ]
then
    echo "Wrong INFRASTRUCTURE_VERSION: $INFRASTRUCTURE_VERSION"
    exit 1
fi

echo $CICD_AGENT
# Remove all folders in mlops not matching exactly CICD_AGENT
FOLDER="./mlops/"
rm -rf $(ls $FOLDER | grep -vxF $CICD_AGENT | sed "s/^/${FOLDER//\//\\/}/")

echo $MLOPS_VERSION
# Delete all experiment folders ending on "SUFFIX"
[[ $MLOPS_VERSION = "aml-cli-v2" ]] && SUFFIX='sdk' || SUFFIX='cli'
FOLDER="./src/"
rm -rf $(ls $FOLDER | grep "$SUFFIX\$" | sed "s/^/${FOLDER//\//\\/}/")
# Delete all folders in the templates of the CICD agent not matching MLOPS_VERSION
FOLDER="./mlops/$CICD_AGENT/templates/"
rm -rf $(ls $FOLDER | grep -vxF $MLOPS_VERSION | sed "s/^/${FOLDER//\//\\/}/")

echo $INFRASTRUCTURE_VERSION
# Delete all folders in infrastructure not INFRASTRUCTURE_VERSION
FOLDER="./infrastructure/"
rm -rf $(ls $FOLDER | grep -vxF $INFRASTRUCTURE_VERSION | sed "s/^/${FOLDER//\//\\/}/")
