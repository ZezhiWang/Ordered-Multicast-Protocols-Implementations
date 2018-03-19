# Ordered-Multicast-Protocols-Implementations
we are exploring three different ordering in multi-cast: FIFO, Total and Casual and simulated a end-to-end interprocess communication by Python to benchmark performance. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
Python 2.7
```


## Running the tests


### Unicast Communication

Testing the send and receive with simulated network delay in Unicast
Create a new process as node i

```
python unicast.py (id)
```
Send msg to a node j

```
send j msg
```
Finish
```
send (id) bye 
```


### Multicast Communication

Testing three different orderings in mulicast: FIFO, Total, Casual in send event 
Create a new process as node i

```
python multicast.py (id) (groupsize) fifo/total/casual
```
Multicast msg

```
send msg
```
Finish
```
send bye 
```

