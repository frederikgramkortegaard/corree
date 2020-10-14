""" Run the test cases seen in ./tests.py to ensure the validity of the corree.py library """

if __name__ == "__main__":

    print("Entering Test Mode:\n ")

    import corree
    from datetime import datetime

    try:
        from tests import cases
    except ImportError:
        logging.error(" >> Could not import ./tests.py")
        exit()

    for enum, case in enumerate(cases):

        if case.name != None:
            print(f" --- '{case.name}' --- ")

        t1 = datetime.now()
        success, args = corree.parse_args(case.inp, case.args)
        t2 = datetime.now()

        print(
            f"""\nTest case [{enum}] gave the following results:
> matching success expectations: {success == case.success},
> matching output expectations: {args == case.output},
> parsing took {t2.microsecond - t1.microsecond} milliseconds to complete,
> and gave the following output dictionary\n >> {args}
        \n"""
        )
