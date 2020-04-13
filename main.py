from Server import Server


def main():
    server = Server('config/config.json')
    server.server_init()


if __name__ == '__main__':
    main()
