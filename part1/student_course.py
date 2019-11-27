import toolkit as tk
import os
import matplotlib.pyplot as plt
import time
import math

#### settings for creating report
PLOT=False
DIST_TIMED=False
TRIALS = 1
CONFLICTS = True
BASIC = False
ADVANCED = True
TIME_REMOVAL = False

def main(plot=PLOT, dist_timed=DIST_TIMED, trials=TRIALS, conflicts=CONFLICTS, basic=BASIC, time_removal=TIME_REMOVAL, advanced=ADVANCED):
    args = tk.get_input()
    fig, ax = plt.subplots(1,3, figsize=(20, 10))
    ax[0].set_xlabel('C'), ax[1].set_xlabel('S'), ax[2].set_xlabel('K')
    ax[0].set_ylabel('Time'), ax[1].set_ylabel('Time'), ax[2].set_ylabel('Time')
    ax[0].set_title('C varying, S:' + str(args.S) + ', K:' + str(args.K) + ', dist: bonus')
    ax[1].set_title('C:' + str(args.C) + ', S: varying, K:' + str(args.K) + ', dist: bonus')
    ax[2].set_title('C:' + str(args.C) + ', S:'+ str(args.S) + ', K: varying, dist: bonus')
    for dist_bonus in ['bonus', 'uniform']:

        args.dist = dist_bonus
        if dist_timed:
            # for plotting
            # fig, ax = plt.subplots(1,3, figsize=(20, 10))
            # ax[0].set_xlabel('C'), ax[1].set_xlabel('S'), ax[2].set_xlabel('K')
            # ax[0].set_ylabel('Time'), ax[1].set_ylabel('Time'), ax[2].set_ylabel('Time')
            # ax[0].set_title('C varying, S:' + str(args.S) + ', K:' + str(args.K) + ', dist:' + args.dist)
            # ax[1].set_title('C:' + str(args.C) + ', S: varying, K:' + str(args.K) + ', dist:' + args.dist)
            # ax[2].set_title('C:' + str(args.C) + ', S:'+ str(args.S) + ', K: varying, dist:' + args.dist)
            for i, param in enumerate(['C', 'S', 'K']):
                if param == 'C':
                    factors = [x*50 + 10 for x in range(0,15)]
                elif param == 'S':
                    factors = [math.ceil(1.4**x + 10) for x in range(0,25)]
                elif param == 'K':
                    factors = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,25,30]
                for trial in range(0,trials):
                    time_stats = []
                    removal_stats = []
                    for factor in factors:
                        if param == 'C':
                            start_time = time.clock()
                            scheduled = tk.scheduled_courses(C=factor, S=args.S, K=args.K, dist=args.dist)
                            elapsed = time.clock() - start_time
                            time_stats.append(elapsed)
                            start_time = time.clock()
                            if basic:
                                edges = tk.conflict_courses(scheduled=scheduled, K=args.K, S=args.S)
                                E, P = tk.basic_removal(edges=edges, C=factor)
                            if advanced:
                                E, P = tk.advanced_removal(scheduled=scheduled, C=factor, K=args.K, S=args.S)
                            elapsed = time.clock() - start_time
                            removal_stats.append(elapsed)
                        elif param == 'S':
                            start_time = time.clock()
                            scheduled = tk.scheduled_courses(C=args.C, S=factor, K=args.K, dist=args.dist)
                            elapsed = time.clock() - start_time
                            time_stats.append(elapsed)
                            start_time = time.clock()
                            if basic:
                                edges = tk.conflict_courses(scheduled=scheduled, K=args.K, S=factor)
                                E, P = tk.basic_removal(edges=edges, C=args.C)
                            if advanced:
                                E, P = tk.advanced_removal(scheduled=scheduled, C=args.C, K=args.K, S=factor)
                            elapsed = time.clock() - start_time
                            removal_stats.append(elapsed)
                        elif param == 'K':
                            start_time = time.clock()
                            scheduled = tk.scheduled_courses(C=args.C, S=args.S, K=factor, dist=args.dist)
                            elapsed = time.clock() - start_time
                            time_stats.append(elapsed)
                            start_time = time.clock()
                            if basic:
                                edges = tk.conflict_courses(scheduled=scheduled, K=factor, S=args.S)
                                E, P = tk.basic_removal(edges=edges, C=args.C)
                            if advanced:
                                E, P = tk.advanced_removal(scheduled=scheduled, C=args.C, K=factor, S=args.S)
                            elapsed = time.clock() - start_time
                            removal_stats.append(elapsed)
                    if time_removal:
                        ax[i].plot(factors, removal_stats)

                        fig.suptitle('Time Study of Matrix Removal ')
                        fig.savefig(args.dist + '_matrix_removal.png')
                    else:
                        if args.dist == 'bonus':
                            ax[i].plot(factors, time_stats, color='black')
                        else:
                            ax[i].plot(factors, time_stats, color='red')
                        fig.savefig(args.dist + '_time_study.png')



    scheduled = tk.scheduled_courses(C=args.C, S=args.S, K=args.K, dist=args.dist)
    # plot class distribution
    if plot:
        tk.plot_distribution(scheduled, classes=args.C, students=args.S, courses_per=args.K, dist=args.dist)
    if conflicts:
        edges = tk.conflict_courses(scheduled=scheduled, K=args.K, S=args.S)
        #print(edges)
    if basic:
        E, P = tk.basic_removal(edges=edges, C=args.C)
    if advanced:
        E, P = tk.advanced_removal(scheduled=scheduled, C=args.C, K=args.K, S=args.S)

    print(E)
    print(P)



if __name__ == '__main__':
    main()
