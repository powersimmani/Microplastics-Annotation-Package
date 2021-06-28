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


1. MP annotation

<p align="center">
  <img src="https://user-images.githubusercontent.com/51187431/123714318-0c2cb680-d8b1-11eb-8e16-45e7cfd94d72.png" width="50%">
</p>

MAP provides manual annotation by users, easily by clicking/dragging the images.

2. Mask generation with different thresholding models

 <img src="https://user-images.githubusercontent.com/51187431/123714294-fc14d700-d8b0-11eb-8626-3630b04abdb8.png" width="50%"><img src="https://user-images.githubusercontent.com/51187431/123714299-fe773100-d8b0-11eb-97fb-7ff62a0732ed.png" width="50%">
 
Depending on the images, the performance of the fluorescent MP labeling differs among the TR models.

 <img src="https://user-images.githubusercontent.com/51187431/123714312-08992f80-d8b1-11eb-9fc8-b501b2648da0.png" width="50%"><img src="https://user-images.githubusercontent.com/51187431/123714313-09ca5c80-d8b1-11eb-8936-d8b1ae8e8a7b.png" width="50%">
 
MAP provides overlay function to overlap the original image on the generated mask with custom transparency, so that the user can qualitatively examine the generated mask.

 <img src="https://user-images.githubusercontent.com/51187431/123714332-10f16a80-d8b1-11eb-8628-dc64f032e431.png" width="50%"><img src="https://user-images.githubusercontent.com/51187431/123714336-12bb2e00-d8b1-11eb-895a-e01d7b9c5fbc.png" width="50%">
 
3. Analysis - graphical visualization & quantitative analysis 

 <img src="https://user-images.githubusercontent.com/51187431/123714349-18b10f00-d8b1-11eb-8cbe-ee1101e18c24.png" width="50%"><img src="https://user-images.githubusercontent.com/51187431/123714355-1b136900-d8b1-11eb-9baa-9757512a800d.png" width="50%">

MAP provide graphical visualization tool where each MP particle is marked with green box and index. This analyzed image can also be saved separately.
And the assigned index directly corresponds to the index in the resulted csv file from quantitative analysis.


## Additional informations

Guide video: https://youtu.be/50GjP9gRza0
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

**We also glad to get the new idea for upgrading software. lease feel free to contact us using 'issues' or following email address: homin.park@ghent.ac.kr**

## References

- Tool making: https://stackoverflow.com/questions/35508711/how-to-enable-pan-and-zoom-in-a-qgraphicsview
- MP-VAT: https://mpvat.wordpress.com/
- processing with image thresholding: 
- U-Net: Ronneberger, O., Fischer, P., & Brox, T. (2015, October). U-net: Convolutional networks for biomedical image segmentation. In International Conference on Medical image computing and computer-assisted intervention (pp. 234-241). Springer, Cham.


## Acknowledgement

The research and development activities described in this paper were funded by Ghent University Global Campus (GUGC) and by the Special Research Fund (BOF) of Ghent University (grant no. 01N01718).

