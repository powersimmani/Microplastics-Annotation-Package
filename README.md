# Microplastics-Annotation-Package (MAP)

## Project
다른 깃 혹은 프로젝트와 연계될 예정임 -> 그릶 추가 
직접 경험하고 비교해보지 않으면 선택이 어려울 수 있다. 따라서 독자들이 실제 MP monitoring process를 수행해 볼 수 있도록  integrated MP annotation / monitoring tool을 제공한다. 이 모델은 다음 4가지를 목표로 하여 제작되었다. 

1. 이미지 편집과 MP annotation 도구를 제공하여 쉽게 오류를 고칠 수 있도록 도와준다. 
2. 다양한 Table~\ref{tbl:method_differences}TR model 사용자가 직접 자동화 툴을 제공하여 사용자가 스스로 비교하고 맞는것을 선택할 수 있게 한다. 
3. Particle count measuring을 시각적으로 분석하게 도와준다. 
4. annotation이 완료된 내용을 쉽게 모델에 학습할 수 있도록 한다. 


## Additional informations

Guide video: ???
More sample images: https://github.com/powersimmani/nile-red-microplastic-images

## Parameter download

For testing our model, please download the file through the following link, unzip it, and add it to the best_model directory. Finally rename the pth file as 'best_model.pth'

* MP-Net : [unet4_best_model.pth](https://drive.google.com/file/d/1wG1WYUtJ49oS0JYVET-33aYvShEKotjf/view?usp=sharing)
* FCN : [fcn_best_model.pth](https://drive.google.com/file/d/1SFhc1G6H0rXEkOXz7q3GM5HBizfr961T/view?usp=sharing)
* Deeplabv3 : [deeplabv3_best_model.pth](https://drive.google.com/file/d/1fbCICTgLOc57z5ETe4Fc6slEBZT9VbiY/view?usp=sharing)
* Nested-UNet : [nested_unet_best_model.pth](https://drive.google.com/file/d/1rTBOZLbK81agYtYVl0WV5Nf2qo6oGFQS/view?usp=sharing)


## For citation

Readers may use the following information to cite our research and the dataset.

Baek, J. Y., de Guzman, M. K., Park, H. M., Park, S., Shin, B., Velickovic, T. C., ... & De Neve, W. (2021). Developing a Segmentation Model for Microscopic Images of Microplastics Isolated from Clams. In Pattern Recognition. ICPR International Workshops and Challenges (pp. 86-97). Springer International Publishing.

**We also glad to get the new idea for upgrading software please feel free to contact us using 'issues' or following email address: homin.park@ghent.ac.kr**

## References

- Tool making: https://stackoverflow.com/questions/35508711/how-to-enable-pan-and-zoom-in-a-qgraphicsview
- MP-VAT: https://mpvat.wordpress.com/
- processing with image thresholding: 
- U-Net: Ronneberger, O., Fischer, P., & Brox, T. (2015, October). U-net: Convolutional networks for biomedical image segmentation. In International Conference on Medical image computing and computer-assisted intervention (pp. 234-241). Springer, Cham.


## Acknowledgement

The research and development activities described in this paper were funded by Ghent University Global Campus (GUGC) and by the Special Research Fund (BOF) of Ghent University (grant no. 01N01718).

