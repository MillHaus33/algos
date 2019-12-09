import argparse
import random
import math
import matplotlib.pyplot as plt
import networkx as nx
import os
import matplotlib.pyplot as plt
import time
from numpy import array

import math


class Node:
    def __init__(self, course, adj_start, degree_start=None, degree=None, deleted=None, nref_degree_list=None, pref_degree_list=None, color=-1, degree_when_deleted=None):
        self.course = course
        self.adj_start = adj_start
        self.degree = degree
        self.degree_start = degree_start
        self.deleted = deleted
        self.nref_degree_list = nref_degree_list
        self.pref_degree_list = pref_degree_list
        self.color = color
        self.degree_when_deleted = degree_when_deleted
        
# Create your dictionary class 
class my_dictionary(dict): 
  
    # __init__ function 
    def __init__(self): 
        self = dict() 
          
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value 
        
        
class LinkedList:
    def __init__(self):
        self.start_node = None

    def traverse_list(self):
        trav = []
        if self.start_node is None:
            print("List has no element")
            return
        else:
            n = self.start_node
            while n is not None:
                trav.append(n.course)
                n = n.ref
            print(trav)
            return trav


    def insert_at_start(self, node):
            new_node = node
            new_node.ref = self.start_node
            self.start_node = new_node

    def insert_at_end(self, data):
            new_node = Node(data)
            if self.start_node is None:
                self.start_node = new_node
                return
            n = self.start_node
            while n.ref is not None:
                n = n.ref
            n.ref = new_node

    def insert_after_item(self, x, data):
        n = self.start_node
        print(n.ref)
        while n is not None:
            if n.item == x:
                break
            n = n.ref
        if n is None:
            print("item not in the list")
        else:
            new_node = Node(data)
            new_node.ref = n.ref
            n.ref = new_node

    def insert_before_item(self, x, data):
        if self.start_node is None:
            print("List has no element")
            return

        if x == self.start_node.item:
            new_node = Node(data)
            new_node.ref = self.start_node
            self.start_node = new_node
            return

        n = self.start_node
        print(n.ref)
        while n.ref is not None:
            if n.ref.item == x:
                break
            n = n.ref
        if n.ref is None:
            print("item not in the list")
        else:
            new_node = Node(data)
            new_node.ref = n.ref
            n.ref = new_node


    def insert_at_index (self, index, data):
        if index == 1:
            new_node = Node(data)
            new_node.ref = self.start_node
            self.start_node = new_node
        i = 1
        n = self.start_node
        while i < index-1 and n is not None:
            n = n.ref
            i = i+1
        if n is None:
            print("Index out of bound")
        else:
            new_node = Node(data)
            new_node.ref = n.ref
            n.ref = new_node
            
            
            
class DoublyLinkedList:
    def __init__(self):
        self.start_node = None
    
    
    def insert_in_emptylist(self, data):
        if self.start_node is None:
            new_node = Node(data)
            self.start_node = new_node
        else:
            print("list is not empty")
    
    
    def insert_at_start(self, node):
        if self.start_node is None:
            new_node = node
            self.start_node = new_node
            return 
        new_node = node
        new_node.nref_degree_list = self.start_node
        self.start_node.pref_degree_list = new_node
        self.start_node = new_node
        return 
    
    def insert_at_end(self, node):
        if self.start_node is None:
            new_node = node
            self.start_node = new_node
            return
        n = self.start_node
        while n.nref_degree_list is not None:
            n = n.nref_degree_list
        new_node = node
        n.nref_degree_list = new_node
        new_node.pref_degree_list = n
        
    
    def insert_after_item(self, x, data):
        if self.start_node is None:
            print("List is empty")
            return
        else:
            n = self.start_node
            while n is not None:
                if n.item == x:
                    break
                n = n.nref
            if n is None:
                print("item not in the list")
            else:
                new_node = Node(data)
                new_node.pref = n
                new_node.nref = n.nref
                if n.nref is not None:
                    n.nref.prev = new_node
                n.nref = new_node
        
        
    def insert_before_item(self, x, data):
        if self.start_node is None:
            print("List is empty")
            return
        else:
            n = self.start_node
            while n is not None:
                if n.item == x:
                    break
                n = n.nref
            if n is None:
                print("item not in the list")
            else:
                new_node = Node(data)
                new_node.nref = n
                new_node.pref = n.pref
                if n.pref is not None:
                    n.pref.nref = new_node
                n.pref = new_node
                
    def traverse_list(self):
        trav = []
        if self.start_node is None:
            print("List has no element")
            return
        else:
            n = self.start_node
            while n is not None:
                trav.append(n.course)
                n = n.nref_degree_list
            print(trav)
                
    
    def delete_at_start(self):
        if self.start_node is None:
            print("The list has no element to delete")
            return 
        if self.start_node.nref_degree_list is None:
            self.start_node = None
            return
        self.start_node = self.start_node.nref_degree_list
        self.start_prev = None;
        
    
    def delete_at_end(self):
        if self.start_node is None:
            print("The list has no element to delete")
            return 
        if self.start_node.nref_degree_list is None:
            self.start_node = None
            return
        n = self.start_node
        while n.nref_degree_list is not None:
            n = n.nref_degree_list
        n.pref_degree_list.nref_degree_list = None
        
        
    def delete_element_by_value(self, x):
        if self.start_node is None:
            print("The list has no element to delete")
            return 
        if self.start_node.nref_degree_list is None:
            if self.start_node.course == x:
                self.start_node = None
            else:
                print("Item not found")
            return 

        if self.start_node.course == x:
            self.start_node = self.start_node.nref_degree_list
            self.start_node.pref_degree_list = None
            return

        n = self.start_node
        while n.nref_degree_list is not None:
            if n.course == x:
                break;
            n = n.nref_degree_list
        if n.nref_degree_list is not None:
            n.pref_degree_list.nref_degree_list = n.nref_degree_list
            n.nref_degree_list.pref_degree_list = n.pref_degree_list
        else:
            if n.course == x:
                n.pref_degree_list.nref_degree_list = None
            else:
                print("Element not found")
                
                
def delete(self, x):
        if self.start_node is None:
            print("The list has no element to delete")
            return 
        if self.start_node.pref_degree_list is None:
            self.start_node = None
            return 
        
        nref_degree_list.pref_degree_list
        
        if self.start_node.course == x:
            self.start_node = self.start_node.nref_degree_list
            self.start_node.pref_degree_list = None
            return

        n = self.start_node
        while n.nref_degree_list is not None:
            if n.course == x:
                break;
            n = n.nref_degree_list
        if n.nref_degree_list is not None:
            n.pref_degree_list.nref_degree_list = n.nref_degree_list
            n.nref_degree_list.pref_degree_list = n.pref_degree_list
        else:
            if n.course == x:
                n.pref_degree_list.nref_degree_list = None
            else:
                print("Element not found")
                
def network_vis2(Edges=None, pos=None, courses_per=None, students=None, classes=None, colors=None, nodes=None):
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(Edges)
    fig, ax = plt.subplots(1, figsize=(10, 10))
    #pos = nx.spring_layout(G,k=0.25,iterations=25)
    
    #print(pos)
    # the histogram of the data
    nx.draw(G, with_labels=True, pos=pos, node_color=colors )
    ax.set_xlabel('Course')
    ax.set_ylabel('Frequency')
    ax.set_title(' Distribution for C: %d, S: %d, K: %d' % (classes, students, courses_per), fontsize=20 )
    plt.show()
    
def network_vis(Edges=None, pos=None, courses_per=None, students=None, classes=None):
    G = nx.Graph()
    G.add_edges_from(Edges)
    fig, ax = plt.subplots(1, figsize=(10, 10))
    #pos = nx.spring_layout(G,k=0.25,iterations=25)
    
    #print(pos)
    # the histogram of the data
    nx.draw(G, with_labels=True, pos=pos)
    ax.set_xlabel('Course')
    ax.set_ylabel('Frequency')
    ax.set_title(' Distribution for C: %d, S: %d, K: %d' % (classes, students, courses_per), fontsize=20 )
    plt.show()
    

def debugger(adj=None, degree_doubly=None, n=None, max_degree=None, pos=None, edges=None):      
    print('course:', n.course)
    delete_list = []
    for x in adj:
        if x.deleted == -1:
            delete_list.append(x.course)
    
    edges2 = edges.copy()
    for edge in edges:
        if edge[0]  in delete_list and edge[1] in delete_list:
            edges2.remove(edge)
        else:
            if edge[0] in delete_list:
                edges2.remove(edge)
            elif edge[1] in delete_list:
                edges2.remove(edge)
    for k in range(0,max_degree+1):
            print("list: ", k)
            degree_doubly[k].traverse_list()
    network_vis(Edges=edges2, pos=pos, courses_per=1, students=1, classes=1)