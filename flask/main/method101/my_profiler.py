
def main():
    import cProfile
    import pstats
    from sefi100 import get_sefi100, sefi_backtest
    from do_analyze import do_analyze

    sefi = get_sefi100()
    print(sefi)
    print("Finished with S5FI")
    result_sef_backtest = sefi_backtest(sefi)
    
    def analysis():
        do_analyze(sefi, result_sef_backtest)
        

    with cProfile.Profile() as pr:
        analysis()

    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    stats.print_stats()
    stats.dump_stats(filename='needs_profiling.prof')


if __name__ == "__main__":
    main()