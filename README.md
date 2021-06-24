# Microplastics-Annotation-Package (MAP)

## Project

With the rising need of automated microplastics (MP) monitoring tool, Microplastics Annotation Package (MAP) tool has been developed. It is a user-friendly tool where the users can perform both MP annotation and monitoring. 

MAP was developed to achieve four objectives:

1. Tool for easy MP annotation by editing the fluorescent MP labeling.
2. Users can easily compare the result of different thresholding (TR) models and select the one that best suits their research purposes or needs.
3. Tool for graphical visualization of counted MP particles.
4. Tool for training the model with user's data.

Below shows a MAP tool caputre with buttons labeled to perform each of four objectives.
<p align="center">
  <img src="https://github.com/powersimmani/Microplastics-Annotation-Package/blob/main/MAP.png" width=70% height=70%>
</p>

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

