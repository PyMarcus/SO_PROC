import random
from queue import Queue
from time import sleep
import sys


def log(text="\nCREATE BY MARCUS"):
    with open('sheduler.log', 'a') as file:
        file.writelines(text)


if sys.version_info.major < 3:
    print("Não compatível com essa versão do python")
    print("Atualize sua versão para 3+")
    sys.exit(0)
# NOTE: The printing methods are old, because I don't know which version of python runs on that poha
# The real times defined by the user to execute were not placed, because,
# if the person sets a high time, it could run for a long time, making the presentation unfeasible.

INTERRUPTION_TIME = 1  # Set the overall system interrupt time to 1
SIZE = 0               # user-defined number of processes


class Process:
    """
    This class represents the process itself.
    That is, when instantiating it, the
    object of the process, each having its own
    attributes.

    The use will be by composition and not inheritance or anything like that.
    Yeah, it's simpler and performative.
    """
    def __init__(self, id, burst, preemtive=False, wait_time=0, priority=random.randint(0, 10)):
        """
        Process attributes
        :param id: filled in automatically, according to the number of processes that will enter.
        :param burst: burst time, that is, how long it will run.
        :param preemtive: variable that identifies whether it is preemptive, that is, if there is an interruption,
         should call the following process.
        """
        self.id = id
        self.burst = burst
        self.preemptive = preemtive
        self.quantum = 1
        self.priority = priority
        self.wait_time = wait_time

    def __repr__(self):
        return "Process {0}:\nBurst: {1}\nPreemptive: {2}\nPriority: {3}\nQuantum: {4}\n".format(
            self.id,
            self.burst,
            self.preemptive,
            self.priority,
            self.quantum
        )


WAIT_QUEUE = Queue()
READY_QUEUE = Queue()


class Sheduler:
    """
    This class represents the process scheduler
    from the CPU.
    Its methods are for, in addition to interacting with the user, initially,
    contain the algorithms, preemptive or not.
    The main methods will be:

    FCFS => FIRST COME FIRST SERVED
    SJF => SHORTEST JOB FIRST
    SRT => SHORTEST REMAINS TIME
    DULING => SHORTEST PRIORITY
    RR => ROUND ROUBIN
    """
    def __init__(self, ready_queue):
        """
        Takes the queue as an argument
        Once this is done, it is traversed and treated in the methods below
        :param ready_queue:
        """
        self.ready_queue = ready_queue

    def __repr__(self):
        return "READY QUEUE FIFO {0}".format(self.ready_queue)

    def __fcfs(self, fscfs_queue, final_queue):
        """
        Method that handles the fcfs algorithm
        If there is no interruption, the processes will be
        executed in the order they arrive. Otherwise,
        as shown in the teacher's image, the processes
        will go to the end of the queue, those who are interrupted
        :param fscfs_queue:
        :param final_queue:
        :return:
        """
        global INTERRUPTION_TIME, SIZE

        total_time = 0
        fscfs_queue_view = self.ready_queue
        history = list()
        # time running
        execute_time = 0
        # capture start time of process execution.
        data = dict()
        # rest that remained to be executed, that is, processes that went to the queue
        rest = dict()
        print('-' * 23, end='')
        print('[FCFS]', end='')
        print('-' * 21)
        print("[+] Processos na fila de espera, por ordem de chegada, aguardando a execucao: \n", flush=True)
        print("*" * 10, flush=True)
        while fscfs_queue_view.qsize() > 0:
            # remove process from the queue to display its details
            proc = fscfs_queue_view.get()
            print(proc)
            # add to the total time, the execution time of each process.
            total_time += proc.burst
            if proc.preemptive:
                proc.wait_time = INTERRUPTION_TIME
            else:
                proc.wait_time = proc.burst
            # store processes to know the execution time of each
            history.append(proc.wait_time)
            print("*" * 10)

        print("[+] Executando escalonamento...")
        print("[+] Duracao estimada de {0}s".format(total_time))
        # traverse the history array
        index = 0
        # while there is a process, run the queue
        while fscfs_queue.qsize() > 0:
            # remove process from queue to run
            proc = fscfs_queue.get()

            # check if there is an interrupt
            if proc.preemptive:
                # if it exists, the process will be sent to the end of the queue, but not before executing for INTERRUPTION_TIME
                print('!' * 10, end='')
                print('INTERROMPIDO P{0}'.format(proc.id), end='')
                print('!' * 10)
                execute_time += INTERRUPTION_TIME
                data[proc.id] = execute_time
                print("[*] Houve interrupcao do processo {0}".format(proc.id))
                print("[+] Esperando por {0}".format(INTERRUPTION_TIME))
                sleep(INTERRUPTION_TIME)
                # remove the history process
                del history[index]
                # reduces the value of INTERRUPTION_TIME in the process burst.
                proc.burst -= INTERRUPTION_TIME
                print("[+] Movendo processo {0} para o final da fila".format(proc.id))
                print("[+] O processo {0} aguardara por {1} s".format(proc.id, sum(history)))
                final_queue.put(proc)

                # skip to the next exit
                continue

            else:
                print("+" * 30)
                print("[*] Interrupcao nao encontrada para o processo {0}".format(proc.id))
                print("[*] Executando P{0} por {1}s".format(proc.id, proc.burst))
                execute_time += proc.burst
                data[proc.id] = execute_time
            index += 1
        print("-" * 50)
        print("[WAIT QUEUE]")
        # running the processes that went to the end of the queue:
        print("[+] Executando os processos que foram para o final da fila")
        # time left to run
        remains = sum(history)
        while final_queue.qsize() > 0:
            proces = final_queue.get()
            print("[+] Retomando o processo {0} aos {1}s".format(proces.id, remains))
            remains += process.burst
            print("[+] Processo {0} executando por {1}s".format(proces.id, proces.burst))
            rest[proces.id] = proces.burst
        print("[+] Concluido")
        print("\n\nRESULTADO [FCFS]:")
        log("\n\nRESULTADO [FCFS]:")
        print("-" * SIZE * 3)
        log("-" * SIZE * 3)
        save = 0
        count = 0
        # average of times (ALLOWS VERIFYING ALGORITHM PERFORMANCE)
        average = 0
        for index, (key, value) in enumerate(data.items()):
            print("P{0} ".format(key), end='')

            if index == 0:
                print("t={0}s ".format(0))
                log("P{0} t={1}s ".format(key, 0))
            else:
                print("t={0}s ".format(save))
                log("P{0} t={1}s ".format(key, save))
            average += save
            count += 1
            save = value
        for index, (key, value) in enumerate(rest.items()):
            print("P{0} ".format(key), end='')
            print("t={0}s ".format(save))
            log("P{0} t={1}s ".format(key, save))
            average += save
            count += 1
            save += value
        print("-" * SIZE * 3)
        log("-" * SIZE * 3)
        print("AVERAGE: {0}".format(average/count))
        log("AVERAGE: {0}".format(average / count))

    def __sjf(self, sjf_queue, sjf_final_queue):
        global sjf_queue_view
        """
        Method that handles the sjf algorithm
        If there is no interruption, the processes will be
        executed so that the one with the shortest time (burst) will execute
        first.Otherwise, as shown in the teacher's image, the processes
        will go to the end of the queue, those who are interrupted

        :param sjf_queue:
        :param sjf_final_queue:
        :return:
        """
        global INTERRUPTION_TIME, SIZE

        total_time = 0
        # sjf_queue_view = self.ready_queue
        history = list()
        # time running
        execute_time = 0
        # capture start time of process execution.
        data = dict()
        # rest that remained to be executed, that is, processes that went to the queue
        rest = dict()
        print('-' * 23, end='')
        print('[SJF]', end='')
        print('-' * 21)
        print("[+] Processos na fila de espera, pelo menor tempo de execucao, aguardando a execucao: \n", flush=True)
        print("*" * 10, flush=True)
        ordered_by_burst_queue = []

        while sjf_queue_view.qsize() > 0:
            # remove process from the queue to display its details
            proc = sjf_queue_view.get()
            # sjf_queue.put(proc)
            ordered_by_burst_queue.append(proc)
            # add to the total time, the execution time of each process.
            total_time += proc.burst
            if proc.preemptive:
                proc.wait_time = INTERRUPTION_TIME
            else:
                proc.wait_time = proc.burst
            # store processes to know the execution time of each
            history.append(proc.wait_time)

        # Here's the difference to the other methods. Below, the sorting by time (burst)
        for n in range(len(ordered_by_burst_queue) - 1):
            for m in range(len(ordered_by_burst_queue) - 1):
                if ordered_by_burst_queue[m].burst > ordered_by_burst_queue[m + 1].burst:
                    aux = ordered_by_burst_queue[m]
                    ordered_by_burst_queue[m] = ordered_by_burst_queue[m + 1]
                    ordered_by_burst_queue[m + 1] = aux

        # display only
        for proc in ordered_by_burst_queue:
            print(proc)
            sjf_queue.put(proc)
            print("*" * 10)

        print("[+] Executando escalonamento...")
        print("[+] Duracao estimada de {0}s".format(total_time))

        # traverse the history array
        index = 0
        # traverse the history array
        while sjf_queue.qsize() > 0:
            # remove process from queue to run
            proc = sjf_queue.get()
            # check if there is an interrupt
            if proc.preemptive:
                # if it exists, the process will be sent to the end of the queue, but not before executing for
                # INTERRUPTION_TIME
                print('!' * 10, end='')
                print('INTERROMPIDO P{0}'.format(proc.id), end='')
                print('!' * 10)
                execute_time += INTERRUPTION_TIME
                data[proc.id] = execute_time
                print("[*] Houve interrupcao do processo {0}".format(proc.id))
                print("[+] Esperando por {0}".format(INTERRUPTION_TIME))
                sleep(INTERRUPTION_TIME)
                # remove the history process
                del history[index]
                # reduces the value of INTERRUPTION_TIME in the process burst.
                proc.burst -= INTERRUPTION_TIME
                print("[+] Movendo processo {0} para o final da fila".format(proc.id))
                print("[+] O processo {0} aguardara por {1} s".format(proc.id, sum(history)))
                sjf_final_queue.put(proc)
                # skip to the next exit
                continue
            else:
                print("+" * 30)
                print("[*] Interrupcao nao encontrada para o processo {0}".format(proc.id))
                print("[*] Executando P{0} por {1}s".format(proc.id, proc.burst))
                execute_time += proc.burst
                data[proc.id] = execute_time
            index += 1
        print("-" * 50)
        print("[WAIT QUEUE]")
        # running the processes that went to the end of the queue:
        print("[+] Executando os processos que foram para o final da fila")
        # time left to run
        remains = sum(history)
        while sjf_final_queue.qsize() > 0:
            proces = sjf_final_queue.get()
            print("[+] Retomando o processo {0} aos {1}s".format(proces.id, remains))
            remains += process.burst
            print("[+] Processo {0} executando por {1}s".format(proces.id, proces.burst))
            rest[proces.id] = proces.burst
        print("[+] Concluido")
        print("\n\nRESULTADO [SJF]:")
        log("\n\nRESULTADO [SJF]:")
        print("-" * SIZE * 3)
        log("-" * SIZE * 3)
        save = 0
        count = 0
        # average of times (ALLOWS VERIFYING ALGORITHM PERFORMANCE)
        average = 0
        for index, (key, value) in enumerate(data.items()):
            print("P{0} ".format(key), end='')
            if index == 0:
                print("t={0}s ".format(0))
                log("P{0} t={1}s ".format(key, save))
            else:
                print("t={0}s ".format(save))
                log("P{0} t={1}s ".format(key, save))
            average += save
            count += 1
            save = value
        for index, (key, value) in enumerate(rest.items()):
            print("P{0} ".format(key), end='')
            print("t={0}s ".format(save))
            log("P{0} t={1}s ".format(key, save))
            average += save
            count += 1
            save += value
        print("-" * SIZE * 3)
        log("-" * SIZE * 3)
        print("AVERAGE: {0}".format(average/count))
        log("AVERAGE: {0}".format(average / count))

    def __duling(self, duling_queue, duling_final_queue):
        """
        Method that handles the duling algorithm
        If there is no interruption, the processes will be
        executed so that the one with the lowest priority will execute
        first.Otherwise, as shown in the teacher's image, the processes
        will go to the end of the queue, those who are interrupted
        :param duling_queue:
        :param duling_final_queue:
        :return:
        """
        global INTERRUPTION_TIME, SIZE, duling_queue_view

        total_time = 0

        history = list()
        # time running
        execute_time = 0
        # capture start time of process execution.
        data = dict()
        # rest that remained to be executed, that is, processes that went to the queue
        rest = dict()
        print('-' * 23, end='')
        print('[DULING]', end='')
        print('-' * 21)
        print("[+] Processos na fila de espera, pela menor prioridade, aguardando a execucao: \n", flush=True)
        print("*" * 10, flush=True)
        ordered_by_priority_queue = []

        while duling_queue_view.qsize() > 0:
            # remove process from the queue to display its details
            proc = duling_queue_view.get()
            # sjf_queue.put(proc)
            ordered_by_priority_queue.append(proc)
            # add to the total time, the execution time of each process.
            total_time += proc.burst
            if proc.preemptive:
                proc.wait_time = INTERRUPTION_TIME
            else:
                proc.wait_time = proc.burst
            # store processes to know the execution time of each
            history.append(proc.wait_time)

        # Here's the difference to the other methods. Below, the sorting by time (burst)
        for n in range(len(ordered_by_priority_queue) - 1):
            for m in range(len(ordered_by_priority_queue) - 1):
                if ordered_by_priority_queue[m].priority > ordered_by_priority_queue[m + 1].priority:
                    aux = ordered_by_priority_queue[m]
                    ordered_by_priority_queue[m] = ordered_by_priority_queue[m + 1]
                    ordered_by_priority_queue[m + 1] = aux

        # display only
        for proc in ordered_by_priority_queue:
            print(proc)
            duling_queue.put(proc)
            print("*" * 10)

        print("[+] Executando escalonamento...")
        print("[+] Duracao estimada de {0}s".format(total_time))

        # traverse the history array
        index = 0
        # while there is a process, run the queue
        while duling_queue.qsize() > 0:
            # remove processo da fila para executar
            proc = duling_queue.get()
            # check if there is an interrupt
            if proc.preemptive:
                # if it exists, the process will be sent to the end of the queue, but not before executing for INTERRUPTION_TIME
                print('!' * 10, end='')
                print('INTERROMPIDO P{0}'.format(proc.id), end='')
                print('!' * 10)
                execute_time += INTERRUPTION_TIME
                data[proc.id] = execute_time
                print("[*] Houve interrupcao do processo {0}".format(proc.id))
                print("[+] Esperando por {0}".format(INTERRUPTION_TIME))
                sleep(INTERRUPTION_TIME)
                # remove the history process
                del history[index]
                # reduces the value of INTERRUPTION_TIME in the process burst.
                proc.burst -= INTERRUPTION_TIME
                print("[+] Movendo processo {0} para o final da fila".format(proc.id))
                print("[+] O processo {0} aguardara por {1} s".format(proc.id, sum(history)))
                duling_final_queue.put(proc)

                # skip to the next exit
                continue
            else:
                print("+" * 30)
                print("[*] Interrupcao nao encontrada para o processo {0}".format(proc.id))
                print("[*] Executando P{0} por {1}s".format(proc.id, proc.burst))
                execute_time += proc.burst
                data[proc.id] = execute_time
            index += 1
        print("-" * 50)
        print("[WAIT QUEUE]")
        # running the processes that went to the end of the queue:
        print("[+] Executando os processos que foram para o final da fila")

        # time left to run
        remains = sum(history)
        while duling_final_queue.qsize() > 0:
            proces = duling_final_queue.get()
            print("[+] Retomando o processo {0} aos {1}s".format(proces.id, remains))
            remains += process.burst
            print("[+] Processo {0} executando por {1}s".format(proces.id, proces.burst))
            rest[proces.id] = proces.burst
        print("[+] Concluido")
        print("\n\nRESULTADO [DULING]:")
        log("\n\nRESULTADO [DULING]:")
        print("-" * SIZE * 3)
        log("-" * SIZE * 3)
        save = 0
        count = 0
        # average of times (ALLOWS VERIFYING ALGORITHM PERFORMANCE):
        average = 0
        for index, (key, value) in enumerate(data.items()):
            print("P{0} ".format(key), end='')
            if index == 0:
                print("t={0}s ".format(0))
                log("P{0} t={1}s ".format(key, save))
            else:
                print("t={0}s ".format(save))
                log("P{0} t={1}s ".format(key, save))
            average += save
            count += 1
            save = value
        for index, (key, value) in enumerate(rest.items()):
            print("P{0} ".format(key), end='')
            print("t={0}s ".format(save))
            log("P{0} t={1}s ".format(key, save))
            average += save
            count += 1
            save += value
        print("-" * SIZE * 3)
        log("-" * SIZE * 3)
        # media is relative to priority and number of processes.
        print("AVERAGE: {0}".format(average/count))
        log("AVERAGE: {0}".format(average / count))

    def finished(self, proc):
        """
        Checks if the process in srt has finished
        the execution, that is, if your working time
        ended.
        :param proc:
        :return:
        """
        if proc.burst == 0:
            print("[+] Processo {0} terminou a execucao".format(proc.id))
            return True
        return False

    def __srt(self, srt_queue, final_srt_queue):
        """
        Method that handles the srt algorithm
        If there is no interruption, the processes will be
        executed so that if there is a process with less work,
        then, the current process is interrupted to execute the other one, until it finishes. Otherwise,
        as shown in the teacher's image, the processes
        will go to the end of the queue, those who are interrupted

        :param srt_queue:
        :param final_srt_queue:
        :return:
        """
        pre_ordered = list()
        ex_time = 0         # tempo estimado

        print('-' * 23, end='')
        print('[SRT]', end='')
        print('-' * 21)
        print("[+] Processos na fila de espera aguardando a execucao: \n", flush=True)
        # feed the vector, to facilitate pre-sorting
        while srt_queue.qsize() > 0:
            proc = srt_queue.get()
            print("*" * 10, flush=True)
            print(proc)
            pre_ordered.append(proc)
            final_srt_queue.put(proc)
            ex_time += proc.burst

        print("[+] Duracao estimada de {0}s".format(ex_time))

        for proc in range(len(pre_ordered) - 1):
            for m in range(len(pre_ordered) - 1):
                if pre_ordered[m].burst < pre_ordered[m + 1].burst:
                    aux = pre_ordered[m]
                    pre_ordered[m] = pre_ordered[m + 1]
                    pre_ordered[m + 1] = aux

        data = dict()
        storange = list()
        amount = 0
        space = 0

        # with the sorted vector,  can now make the comparisons
        while final_srt_queue.qsize() > 0:
            _process = final_srt_queue.get()
            if self.finished(_process):
                continue
            space += 1
            if _process.preemptive:
                print("[+] Executando o processo {0} por {1}s".format(_process.id, INTERRUPTION_TIME))
                sleep(INTERRUPTION_TIME)
                _process.burst -= INTERRUPTION_TIME
                # go back to the end of the queue
                print("[+] Movendo o processo {0} para o final da fila".format(_process.id))
                final_srt_queue.put(_process)
                # remove preemption from the process, since it has already been executed
                _process.preemptive = False
                amount += INTERRUPTION_TIME
                data[str(_process.id) + ' ' * space] = amount
                storange.append(data)
                # skip to the next
                continue
            else:
                if pre_ordered[len(pre_ordered) - 1].id == _process.id:
                    print("[+] Executando processo {0} por {1}s".format(_process.id, _process.burst))
                    print("[+] Processo {0} terminou a execucao!".format(_process.id))
                    # if equal, remove from vector
                    pre_ordered.pop()
                    amount += _process.burst
                    data[str(_process.id) + ' ' * space] = amount
                    storange.append(data)
                else:
                    print("[!] Encontrado processo com menor trabalho.")
                    print("[+] Executando processo {0} por {1}s".format(_process.id, INTERRUPTION_TIME))
                    _process.burst -= INTERRUPTION_TIME
                    print("[+] Buscando processo de menor espaço de tempo na CPU...")
                    print("[+] Encontrado.")
                    print("[+] Movendo o processo {0} para o final da fila".format(_process.id))
                    final_srt_queue.put(_process)
                    amount += INTERRUPTION_TIME
                    data[str(_process.id) + ' ' * space] = amount
                    storange.append(data)

        # result display

        # avoid repetition
        show = set()

        print("[+] Concluido")
        print("\n\nRESULTADO [SRT]:")
        log("\n\nRESULTADO [SRT]:")
        print("-" * SIZE * 3)
        log("-" * SIZE * 3)
        save = 0
        count = 0
        # average of times (ALLOWS VERIFYING ALGORITHM PERFORMANCE):
        average = 0
        for proc in storange:
            for index, (key, value) in enumerate(proc.items()):
                # if it has repeated, it will be disregarded
                if key in show:
                    continue
                show.add(key)
                print("P{0} ".format(key.strip()), end='')
                if index == 0:
                    print("t={0}s ".format(0))
                    log("P{0} t={1}s ".format(key, save))
                else:
                    print("t={0}s ".format(save))
                    log("P{0} t={1}s ".format(key, save))
                average += save
                count += 1
                save = value
        print("-" * SIZE * 3)
        log("-" * SIZE * 3)
        # media is relative to priority and number of processes.
        print("AVERAGE: {0}".format(average / count))
        log("AVERAGE: {0}".format(average / count))

    @staticmethod
    def _aux(process_rr, proc):
        """
        [PROTECTED]Helper function to avoid massive repetition in the same code
        calculates the estimated time for the process to return to the processor
        :param process:
        :return:
        """
        temp = 0
        for procc in process_rr:
            if procc.id == proc.id:
                continue
            elif procc.preemptive:
                temp += 1
            else:
                temp += procc.burst
        print("[+] O processo {0} poderá aguardar por {1} s".format(proc.id, temp))

    def __robin_round(self, rr_queue, final_rr_queue):
        global INTERRUPTION_TIME, SIZE
        """
        Method that handles the robin round algorithm
        If there is no interruption, the processes will be
        executed based on the quantum. Otherwise,
        as shown in the teacher's image, the processes
        will go to the end of the queue, those who are interrupted
        :return:
        """
        total_time = 0
        rr_queue_view = self.ready_queue
        # time running
        execute_time = 0
        print('-' * 23, end='')
        print('[RR]', end='')
        print('-' * 21)
        print("[+] Processos na fila de espera, pelo quantum, aguardando a execucao: \n", flush=True)
        print("*" * 10, flush=True)

        # store , exclusively, to measure the return time of the interrupted process
        process_rr = set()
        while rr_queue_view.qsize() > 0:
            # remove process from the queue to display its details
            proc = rr_queue_view.get()
            print(proc)
            process_rr.add(proc)
            # add to the total time, the execution time of each process.
            total_time += proc.burst
            if proc.preemptive:
                proc.wait_time = INTERRUPTION_TIME
            else:
                proc.wait_time = proc.burst
            print("*" * 10)

        # list to store processes in order and display them later
        results = []

        print("[+] Executando escalonamento...")
        print("[+] Duracao estimada de {0}s".format(total_time))
        # traverse the history array
        index = 0
        # while there is a process, run the queue
        while rr_queue.qsize() > 0:

            # remove process from queue to run
            proc = rr_queue.get()

            # capture start time of process execution.
            data = dict()

            # check if there is still runtime for the process in question
            if proc.burst > 0:
                # check if there is an interrupt
                if proc.preemptive:

                    # if it exists, the process will be sent to the end of the queue, but not before executing for
                    # INTERRUPTION_TIME
                    print('!' * 10, end='')
                    print('INTERROMPIDO P{0}'.format(proc.id), end='')
                    print('!' * 10)
                    execute_time += INTERRUPTION_TIME
                    data[proc.id] = execute_time
                    print("[*] Houve interrupcao do processo {0}".format(proc.id))
                    print("[+] Esperando por {0}s".format(INTERRUPTION_TIME))
                    sleep(INTERRUPTION_TIME)
                    # reduces the value of INTERRUPTION_TIME in the process burst.
                    proc.burst -= INTERRUPTION_TIME
                    print("[+] Movendo processo {0} para o final da fila".format(proc.id))
                    results.append(data)
                    # removing need for forced interrupt, after one has already been performed
                    proc.preemptive = False

                    # analyzing the possible waiting time of this interrupted process in the queue,
                    # before the next run
                    self._aux(process_rr, proc)

                    # return to the end of the queue
                    rr_queue.put(proc)
                    # skip to the next exit
                    continue
                else:
                    print("+" * 30)
                    print("[*] Interrupcao forçada nao encontrada para o processo {0}".format(proc.id))
                    print("[!] Porem, como este algoritmo e preemptivo, sera interrompido por {0}s".
                          format(INTERRUPTION_TIME))
                    proc.burst -= INTERRUPTION_TIME
                    print("[*] Executando P{0} por {1}s".format(proc.id, INTERRUPTION_TIME))
                    print("[*] Processo {0} retornando ao final da fila...".format(proc.id))

                    # analyzing the possible waiting time of this interrupted process in the queue,
                    # before the next run
                    self._aux(process_rr, proc)

                    execute_time += proc.quantum
                    data[proc.id] = 1
                    results.append(data)

                    # return to the end of the queue
                    rr_queue.put(proc)
                index += 1
            else:
                print("[+] O processo {0} terminou a sua execucao".format(proc.id))

        # display the result
        print("\n[+] Resultado [RR]")
        log("\n\nRESULTADO [RR]:")
        print("-" * SIZE * 3)
        log("-" * SIZE * 3)
        save = 0
        # average of times (ALLOWS VERIFYING ALGORITHM PERFORMANCE)
        average = 0
        index = 0

        # will save the processes, without repetition, to calculate the time precisely.
        # as said in class, though, it doesn't make much sense
        different_p = set()
        # corresponding time
        different_t = set()
        for result in results:
            for (key, value) in result.items():
                print("P{0} ".format(key), end='')
                different_p.add(key)
                different_t.add(save)
                if index == 0:
                    print("t={0}s ".format(0))
                    log("P{0} t={1}s ".format(key, save))
                else:
                    print("t={0}s ".format(save))
                    log("P{0} t={1}s ".format(key, save))
                save += INTERRUPTION_TIME
            index += 1
        print("-" * SIZE * 3)
        log("-" * SIZE * 3)
        for n in range(len(different_p)):
            # add the matches, before starting to repeat
            average += different_t.pop()
        print("AVERAGE: {0}".format(average / SIZE))
        log("AVERAGE: {0}".format(average / SIZE))

    def start(self):
        """
        Calls the private methods of the M algorithms
        and start operations
        :return:
        """
        global fscfs_queue, final_queue, sjf_queue, final_sjf_queue, duling_queue, final_duling_queue_queue, srt_queue,\
            final_srt_queue, rr_queue, final_rr_queue
        # --------------- FCFS ----------------
        self.__fcfs(fscfs_queue, final_queue)
        print('-' * 50)
        # --------------- SJF -----------------
        self.__sjf(sjf_queue, final_sjf_queue)
        print('-' * 50)
        # -------------- Dulling --------------
        self.__duling(duling_queue, final_duling_queue_queue)
        print('-' * 50)
        # -------------- SRT --------------
        self.__srt(srt_queue, final_srt_queue)
        print('-' * 50)
        # -------------- RR --------------
        self.__robin_round(rr_queue, final_rr_queue)
        print('-' * 50)


if __name__ == '__main__':
    sjf_queue_view = Queue()
    duling_queue_view = Queue()
    fscfs_queue = Queue()
    final_queue = Queue()
    sjf_queue = Queue()
    final_sjf_queue = Queue()
    duling_queue = Queue()
    final_duling_queue_queue = Queue()
    srt_queue = Queue()
    final_srt_queue = Queue()
    rr_queue = Queue()
    final_rr_queue = Queue()

    # user interaction V
    log("SHEDULER\n")
    try:
        how_many_process = int(input("[+] Quantos processos serao executados? "))
        # R
        SIZE = how_many_process
        for amount in range(how_many_process):
            time = int(input("[+] Tempo para o processo {0}: ".format(amount)))
            interruption = bool(input("[+] O processo {0} sera interrompido? [sim/nao] ".format(amount)).lower()
                                .replace('sim', 'True')\
                                .replace('nao', ''))
            process = Process(id=amount,
                              burst=time,
                              preemtive=interruption,
                              priority=random.randint(0, 10))
            READY_QUEUE.put(process)
            fscfs_queue.put(process)
            sjf_queue_view.put(process)
            srt_queue.put(process)
            rr_queue.put(process)
            duling_queue_view.put(process)
        print('-' * 50)

        # save the queue in scheduler A
        sheduler = Sheduler(READY_QUEUE)
        sheduler.start()
        log()

    except ValueError as e:
        print("[-] Entrada invalida! {0}".format(e))
