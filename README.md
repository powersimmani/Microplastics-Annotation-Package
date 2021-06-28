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

수정중입니다-백지연
![Slide_7](https://user-images.githubusercontent.com/51187431/123610307-70149800-d83b-11eb-9a47-c32ac7d6cc3a.png)
![Slide_8](https://user-images.githubusercontent.com/51187431/123610387-83276800-d83b-11eb-95e5-ef7373d18088.png)
![Slide_10](https://user-images.githubusercontent.com/51187431/123610411-8884b280-d83b-11eb-9531-45d6d8a30c6b.png)
![Slide_11](https://user-images.githubusercontent.com/51187431/123610414-891d4900-d83b-11eb-9adb-b7ee58c79e20.png)
![Slide_16](https://user-images.githubusercontent.com/51187431/123610439-8e7a9380-d83b-11eb-979d-78c38a0153de.png)
![Slide_17](https://user-images.githubusercontent.com/51187431/123610446-8fabc080-d83b-11eb-8b15-aef9662bc878.png)
![Slide_21](https://user-images.githubusercontent.com/51187431/123610474-94707480-d83b-11eb-94f2-ac10e5546c12.png)
![Slide_25](https://user-images.githubusercontent.com/51187431/123610478-95a1a180-d83b-11eb-9e4e-6940ec14cba9.png)
![Slide_27](https://user-images.githubusercontent.com/51187431/123610484-96d2ce80-d83b-11eb-901f-0edeaeabc511.png)

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

