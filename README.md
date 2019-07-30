# A simple software for processing hyperspectral data
## Introduction
This is the source code of our data processing tool that  we use in our paper [(Apple Surface Pesticide Residue Detection Method Based on Hyperspectral Imaging)](https://link.springer.com/chapter/10.1007/978-3-030-02698-1_47) for processing hyperspectral data.

It still has some bugs to fix and some features to be implemented. 

The code written at the time was very messy. Recently, I will try to make the code clearer to read and easier to maintain.

## Requirements
- Python3
- PyQt5
- numpy
- pandas
- python-opencv

## ToDo List
- [ ] Rearrange the code structure, make it easier to maintain
- [ ] Rewrite the code of manually select the ROI(Region Of Interest)
- [ ] Support 'bil' format hyperspectral data
- [ ] ...


## Finished
- [x] Read and display basic information of 'raw' format data 
- [x] Display spectral curve
- [x] Select a region of interest (Our target is Apple, so we use Hough Circle Transform)
- [x] Category classification(Also designed for our work)
- [x] ...

## How To Run
```bash
python Main.py
```

## Citation
If you find our work useful, you could cite our paper，thanks! 😊😊).
```
@InProceedings{Jia2018PesticideDetection,
	author="Jia, Yaguang and He, Jinrong and Fu, Hongfei and Shao, Xiatian and Li, Zhaokui",
	title="Apple Surface Pesticide Residue Detection Method Based on Hyperspectral Imaging",
	booktitle="Intelligence Science and Big Data Engineering",
	year="2018",
	publisher="Springer International Publishing",
	address="Cham",
	pages="539--556",
	isbn="978-3-030-02698-1"
}
```
## Preview

![main](/img/Window.png)

![main](/img/1.gif)

![main](/img/2.gif)

![main](/img/3.gif)

![main](/img/4.gif)

![main](/img/5.gif)

![main](/img/6.gif)

![main](/img/7.gif)

