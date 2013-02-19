# coding: utf-8


import os


def main():
    projectdir = os.path.dirname(__file__)
    manage = os.path.join(projectdir, "manage.py")
    os.chmod(manage, 0755)


if __name__ == "__main__":
    main()
