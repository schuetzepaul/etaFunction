# etaFunction
Toy MC to study the effects of noise and threshold on the silicon strip sensor resolution for sensors with a linear eta function.

An input position is drawn from a uniform random distribution within two half strips, hence ranging from -d/2 to d/2 with the strip pitch d. The strip charge for both stips is calculated from a linear eta function, noise is added and a threshold is applied. The reconstructed position is then the center of gravity of both strip charges. A histogram compares the reconstructed position with the known truth.


## Usage

```
python eta.py -e 10000 -n 200 -t 1000
```
will create 10000 particles, add 200 electron gaussian noise and apply a 1000 electron threshold.