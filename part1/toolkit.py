import argparse
import random
import math
import matplotlib.pyplot as plt
import networkx as nx




def get_input():
    # custom checks used code from
    # https://stackoverflow.com/questions/18700634/python-argparse-integer-condition-12
    def course_check(x):
        x = int(x)
        if x > 10000:
            raise argparse.ArgumentTypeError("Max courses is 10,000")
        return x
    def student_check(x):
        x = int(x)
        if x > 100000:
            raise argparse.ArgumentTypeError("Max students is 100,000")
        return x
    parser = argparse.ArgumentParser(description='Project Part 1')
    parser.add_argument('-C',
                        type=course_check,
                        help='Number of courses being offered')
    parser.add_argument('-S',
                        type=student_check,
                        help='Number of students')
    parser.add_argument('-K',
                        type=int,
                        help='Number of courses per student')
    parser.add_argument('-dist',
                        type=str,
                        help='Distribution',
                        choices=['uniform', 'skewed', '4tier', 'piecewise', 'bonus'])
    args = parser.parse_args()
    # input check
    if args.K > args.C:
        raise Exception("""Number of courses must be greater
                           than number of courses per student.""")
    return args


def scheduled_courses(dist=None, C=None, K=None, S=None):
        scheduled = []
        course_list = [x for x in range(0, C)]
        if dist=='4tier':
            tier_size = math.ceil(C/4)
            pmf = ([.4 / C for x in range(0, tier_size)] + [.3 / C for x in range(0, tier_size)] + [.2 / C for x in range(0, tier_size)] + [.1 / C for x in range(0, tier_size)])
            pmf = pmf[0:C]
        schedule = 0
        for i in range(0,S):
            course_options = course_list
            # implementation of fisher and yates shuffle
            for j in range(0,K):
                if dist=='uniform' or dist=='skewed' or dist=='piecewise':
                    course, course_index = course_generator(dist=dist, N=C-j-1, course_options=course_options, C=C)
                    scheduled.append(course)
                    course_options[course_index] = course_options[-1-j]
                    course_options[-1-j] = course
                elif dist=='4tier' :
                    course, course_index = course_generator(dist=dist, N=C-j-1, course_options=course_options, pmf=pmf, C=C)
                    scheduled.append(course)
                    course_options[course_index] = course_options[-1-j]
                    course_options[-1-j] = course
                    p = pmf[-1-j]
                    pmf[-1-j] = pmf[course_index]
                    pmf[course_index] = p
                elif dist=='bonus':
                    course, course_index = course_generator(dist=dist, N=C, course_options=course_list, C=C)
                    x = 0
                    if j ==0:
                        scheduled.append(course)
                        schedule = schedule + 1
                    else:
                        for k in range(schedule-j,schedule-1):
                            if course == scheduled[k]:
                                x = 1
                        if x  == 1:
                            course, course_index = course_generator(dist=dist, N=C, course_options=course_list, C=C)
                        else:
                            scheduled.append(course)
                            schedule = schedule + 1
                    course_options[course_index] = course_options[-1-j]
                    course_options[-1-j] = course

        return scheduled

def course_generator(dist=None, N=None, course_options=None, pmf=None, C=None):
    if dist=='uniform':
        course_index = random.randint(0, N)
        course = course_options[course_index]
    elif dist=='skewed':
        course_index_1 = random.randint(0, N)
        course_index_2 = random.randint(0, N)
        course_1 = course_options[course_index_1]
        course_2 = course_options[course_index_2]
        if course_1 <= course_2:
            course_index = course_index_1
            course = course_1
        else:
            course, course_index = course_generator(dist=dist, N=N, course_options=course_options, C=C)
    # used some personal lecture notes for this
    elif dist=='4tier':
        pmf = pmf[0:N+1]
        max_p = pmf[0]
        for x in pmf:
            if x > max_p:
                max_p = x
        course_index_1 = random.randint(0, N)
        course_index_2 = random.randint(0, N)
        u1 = pmf[course_index_1]
        u2 = course_index_2 / N
        course_1 = course_options[course_index_1]
        course_2 = course_options[course_index_2]
        if u2 < (u1 / max_p):
            course_index = course_index_1
            course = course_1
        else:
            course, course_index = course_generator(dist=dist, N=N, course_options=course_options, pmf=pmf, C=C)
    elif dist=='piecewise':
        course_index_1 = random.randint(0, N)
        course_index_2 = random.randint(0, N)
        course_1 = course_options[course_index_1]
        course_2 = course_options[course_index_2]
        if course_1 <= course_2  + C/2:
            course_index = course_index_1
            course = course_1
        else:
            course, course_index = course_generator(dist=dist, N=N, course_options=course_options, C=C)
    elif dist=='bonus':
        course_index = random.randint(0, C-1)
        course = course_options[course_index]
    # used some personal lecture notes for this
    return course, course_index


def plot_distribution(scheduled=None, classes=None, students=None, courses_per=None, dist=None):
    # for plotting
    fig, ax = plt.subplots(1)
    # the histogram of the data
    n, bins, patches = ax.hist(scheduled, classes)
    ax.set_xlabel('Course')
    ax.set_ylabel('Frequency')
    ax.set_title(dist + ' Distribution for C: %d, S: %d, K: %d' % (classes, students, courses_per) )
    fig.savefig('output_' + dist + '.png')

def conflict_courses(scheduled=None, K=None, S=None):
    edges = []
    y = 0
    for i in range(0, (K * S), K):
        sched = scheduled[i:i+K]
        for j in range(0, K):
            a = sched[j]
            for k in range(j+1, K):
                if a < sched[k]:
                    x = (a, sched[k])
                else:
                    x = (sched[k], a)
                edges.append(x)
                y += 1
    #print('Total number of conflicts: ' + str(y))
    return edges


def basic_removal(edges=None, C=None):
    E = [[-1] for c in range(C)]
    course_counter = [1 for x in range(0, C)]
    starter_counter = [0 for x in range(0, C)]
    P = []
    for edge in edges:
        a = edge[0]
        b = edge[1]
        for i in range(0, course_counter[a]):
            x = 0
            if E[a][i] == b:
                x = 1
            if x == 1:
                break
        if x == 0:
            if E[a][0] == -1 & E[b][0] == -1:
                E[a][0] = b
                E[b][0] = a
                starter_counter[b] = starter_counter[b] + 1
                starter_counter[a] = starter_counter[a] + 1
            else:
                if E[a][0] == -1 or E[b][0] == -1:

                    if E[a][0] == -1:
                        E[a][0] = b
                        E[b].append(a)
                        course_counter[b] = course_counter[b] + 1
                        starter_counter[b] = starter_counter[b] + 1
                        starter_counter[a] = starter_counter[a] + 1
                    elif E[b][0] == -1:
                        E[b][0] = a
                        E[a].append(b)
                        course_counter[a] = course_counter[a] + 1
                        starter_counter[b] = starter_counter[b] + 1
                        starter_counter[a] = starter_counter[a] + 1
                else:
                    E[a].append(b)
                    E[b].append(a)
                    course_counter[a] = course_counter[a] + 1
                    course_counter[b] = course_counter[b] + 1
                    starter_counter[b] = starter_counter[b] + 1
                    starter_counter[a] = starter_counter[a] + 1

    E_final = []
    for i in range(0, C):
        if starter_counter[i] > 0:
            for j in range(0, course_counter[i]):
                E_final.append(E[i][j])
    P_final = [0]
    x = 0
    for i in range(0, C):
        if starter_counter[i] > 0:
            x += 1
        P_final.append(P_final[-1] + starter_counter[i])



    #print('Unique number of conflicts: ' + str(x))
    # print(P_final)
    # print(E_final)
    return E_final, P_final

def advanced_removal(scheduled=None, K=None, S=None, C=None):
    P_final = [0]
    E_final = []
    edges = []
    a_matrix = [[0 for x in range(0, C)] for y in range(0, C)]
    y = 0
    for i in range(0, (K * S), K):
        sched = scheduled[i:i+K]
        for j in range(0, K):
            a = sched[j]
            for k in range(j+1, K):
                if a_matrix[a][sched[k]] == 0 or a_matrix[sched[k]][a] == 0:
                    a_matrix[a][a] = a_matrix[a][a] + 1
                    a_matrix[sched[k]][sched[k]] = a_matrix[sched[k]][sched[k]] + 1
                a_matrix[a][sched[k]] = a_matrix[a][sched[k]] + 1
                a_matrix[sched[k]][a] = a_matrix[sched[k]][a] + 1

                y += 1

    #print('Total number of conflicts: ' + str(y))
    j = 0
    for z in range(0,C):
        P_final.append(P_final[-1] + a_matrix[z][z])
        for b in range(0,C):
            if z != b:
                if a_matrix[z][b] > 0:
                    E_final.append(b)
                    j += 1
    #print('Unique number of conflicts: ' + str(j/2))



    # print(P_final)
    # print(E_final)
    return E_final, P_final


def network_vis(Edges=None, courses_per=None, students=None, classes=None):
    G = nx.Graph()
    G.add_edges_from(Edges)
    fig, ax = plt.subplots(1, figsize=(10, 10))
    pos = nx.spring_layout(G,k=0.25,iterations=25)
    # the histogram of the data
    nx.draw(G, with_labels=True, pos=pos )
    ax.set_xlabel('Course')
    ax.set_ylabel('Frequency')
    ax.set_title(' Distribution for C: %d, S: %d, K: %d' % (classes, students, courses_per), fontsize=20 )
    fig.savefig('graph.png')
