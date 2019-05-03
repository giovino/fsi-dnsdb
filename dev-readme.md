## Development Instructions

1.  Clone the fsi-dnsdb repository
    ```text
    $ git clone https://github.com/giovino/fsi-dnsdb.git
    $ cd fsi-dnsdb
    ```
1.  Start vagrant
    ```text
    $ vagrant up
    $ vagrant ssh
    ```
1.  Reboot the machine using `poweroff` and `vagrant up` to finish updating the VM (first time only)
    ```text
    $ sudo poweroff
    <wait 10 seconds>
    $ vagrant up
    $ vagrant ssh
    ```
1.  Install in development mode using Poetry
    ```text
    $ cd /vagrant
    $ poetry install
    ```
1.  Open a shell within the virtual environment using Poetry
    ```text
    $ poetry shell
    ```
1.  Open ipython and load the `dnsdb` module
    ```text
    $ ipython
    In [1]: import dnsdb
    ```
