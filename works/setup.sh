USERNAME=$1

curl -sSL https://install.python-poetry.org | python3 -
echo 'export PATH="/home/$USERNAME/.local/bin:$PATH"' >> ~/.bashrc
export PATH="/home/$USERNAME/.local/bin:$PATH"

# Write special code below this for the environment you want to build.

# Install ANTLR

# 1. Install java
sudo apt update
sudo apt upgrade -y
sudo apt install openjdk-17-jdk -y
echo -e "JAVA_HOME=\$(readlink -f /usr/bin/javac | sed \"s:/bin/javac::\")
export JAVA_HOME
PATH=\$PATH:\$JAVA_HOME/bin
export PATH" >> ~/.bashrc

# 2. Download ANTLR
sudo curl -sS -o /usr/local/lib/antlr-4.13.1-complete.jar https://www.antlr.org/download/antlr-4.13.1-complete.jar

# 3. add to the path to ANTLR
echo 'export CLASSPATH=".:/usr/local/lib/antlr-4.13.1-complete.jar:$CLASSPATH"' >> ~/.bashrc

# 4. set alias
echo "alias antlr4='java -Xmx500M -cp "/usr/local/lib/antlr-4.13.1-complete.jar:\$CLASSPATH" org.antlr.v4.Tool'"  >> ~/.bashrc
echo "alias grun='java -Xmx500M -cp "/usr/local/lib/antlr-4.13.1-complete.jar:\$CLASSPATH" org.antlr.v4.gui.TestRig'" >> ~/.bashrc

# Install Taskfile
sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b ~/.local/bin
