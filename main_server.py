from src.server_application import ServerApplication

if __name__ == "__main__":
    import cProfile

    pr = cProfile.Profile()
    pr.enable()

    ServerApplication()

    pr.disable()
    pr.print_stats(sort='time')
