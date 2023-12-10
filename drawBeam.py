##Automation of Continuous Beam Drawing on Autocad 
## using #BasicPYTHON #PYAUTOCAD

from pyautocad import Autocad, APoint
acad=Autocad()     ###create_if_not_exists=True

print(acad.doc.Name)
doc=acad.ActiveDocument
ms=doc.ModelSpace

# creating a new layer
def create_layer(name, color):
    layer = acad.ActiveDocument.Layers.Add(name)
    layer.color = color

create_layer('Beam_LSection', 1)  # Color index 1 represents red. Change it according to your requirements.
create_layer('text', 2)
create_layer('Long_repar', 3)
create_layer('rebar_section',4)
create_layer('strrp',5)
create_layer('Stirrups_sides',6)
create_layer('Stirrups_center',7)
create_layer('Section_line',8)
create_layer('Beam_CSection',9)

z=0
N=int(input('Enter No Of Storey : '))

##Functions for Drawing....
if 'Long_rebar' not in [layer.Name for layer in acad.ActiveDocument.Layers]:
    new_layer = acad.ActiveDocument.Layers.Add('Long_rebar')


def draw(p1x,p1y,p2x,p2y):
    for j in range(len(p1x)):
        p1=APoint(p1x[j],p1y[j]+z)
        p2=APoint(p2x[j],p2y[j]+z)
        line1=acad.model.AddLine(p1,p2)
        line1.layer='Beam_LSection' 
        
def l_dimdraw(long_dim_x0,long_dim_y0,long_dim_x1,long_dim_y1):
    for j in range(len(long_dim_x0)):
        p1=APoint(long_dim_x0[j],long_dim_y0[j]+z)
        p2=APoint(long_dim_x1[j],long_dim_y1[j]+z)
        line1=acad.model.AddLine(p1,p2)
        line1.layer='text' 
           
def draw_longitudinal_rebar(p1x,p1y,p2x,p2y):
    for j in range(len(p1x)):
        p1=APoint(p1x[j],p1y[j]+z)
        p2=APoint(p2x[j],p2y[j]+z)
        line1=acad.model.AddLine(p1,p2)
        line1.layer='Long_rebar'
        
def draw_without_cantilever(column_width,column_cc,a,a_initial,d,beam_cc):
    ###---lower longitdudinal rebar(first three points---------##----
    p3x=[a_initial-column_width+column_cc,a_initial-column_width+column_cc,a-column_cc,a_initial-column_width+column_cc,a_initial-column_width+column_cc,a-column_cc]
    p3y=[beam_cc,beam_cc,beam_cc,d-beam_cc,d-beam_cc,d-beam_cc]

    p4x=[a_initial-column_width+column_cc,a-column_cc,a-column_cc,a_initial-column_width+column_cc,a-column_cc,a-column_cc]
    p4y=[d*2,beam_cc,d*2,-d,d-beam_cc,-d]
    
    drawing_1=draw_longitudinal_rebar(p3x,p3y,p4x,p4y)

##For Stirrups Details .....
beam_cc=20
cc=beam_cc

def stirrup(l_next,z,d,cc,a):

    l=l_next
##For stirrups
    print('')
    print('For stirrups : ')
    spacing_left=int(input('Enter Spacing(mm) on left section(l/3) of Beam : '))
    spacing_center=int(input('Enter Spacing(mm) on center section of Beam  : '))
    spacing_right=int(input('Enter Spacing(mm) on right section(l/3) of Beam  : '))
    
    print('')
    sp=0
            
   ##ForStirrups
    #print('')
    #print('**********Stirrup Diameter***********')
    #print('')
    stirrup_dia=8#int(input('Enter diameter of stirrup : '))
    for j in range(3):
        if j==0:
                n_left=round(((l/3-50*2)/spacing_left))+1
                 ##Annotation
                ##inclined line
                ptext_1=APoint(a+l/6,d/2+z)
                ptext_2=APoint(a+l/6+46.6,-86.4+z)
                #Line1
                line1=acad.model.AddLine(ptext_1,ptext_2)
                line1.layer='text'
                ##Flat line
                ptext_3=APoint(a+l/6+46.6,-86.4+z)
                ptext_4=APoint(a+46.6+77+l/6,-86.4+z)
                line2=acad.model.AddLine(ptext_3,ptext_4)
                line2.layer='text'
                ##Text To beshown
                text_dim=[n_left,stirrup_dia,spacing_left]
                text_length=acad.model.AddText(' %s-%smmdia@%smm c/c'%(text_dim[0],text_dim[1],text_dim[2]),ptext_4,25)
                text_length.layer='text'

                
                ##Stirrup lines @middle
                ptext_5=APoint(a+l/6-250,d/2+z)
                ptext_6=APoint(a+l/6+250,d/2+z)
                line3=acad.model.AddLine(ptext_5,ptext_6)
                line3.layer='strrp'
                
                for j in range(n_left):
                    if j == 0:
                            p3=APoint(a+50,cc+z)
                            p4=APoint(a+50,z+d-cc)
                            line=acad.model.AddLine(p3,p4)
                            line.layer='Stirrups_sides'
                            sp=sp+50
                           # print(sp)
                    else:
                            sp=sp+spacing_left
                            #print(sp)
                            p3=APoint(a+sp,z+cc)
                            p4=APoint(a+sp,z+d-cc)
                            line=acad.model.AddLine(p3,p4)
                            line.layer='Stirrups_sides'    
         
        elif j==1:
                n_center=round(((l/3-50*2)/spacing_center))+1
                ##inclined line
                ptext_1=APoint(a+l/2,d/2+z)
                ptext_2=APoint(a+46.6+l/2,d+z+86.4)
                #Line1
                line1=acad.model.AddLine(ptext_1,ptext_2)
                line1.layer='text'
                ##Flat line
                ptext_3=APoint(a+46.6+l/2,d+z+86.4)
                ptext_4=APoint(a+46.6+77+l/2,d+z+86.4)
                line2=acad.model.AddLine(ptext_3,ptext_4)
                line2.layer='text'
                ##Text To beshown
                text_dim=[n_center,stirrup_dia,spacing_center]
                text_length=acad.model.AddText(' %s-%smmdia@%smm c/c'%(text_dim[0],text_dim[1],text_dim[2]),ptext_4,25)
                text_length.layer='text'
                
                ##Stirrup lines @middle
                ptext_5=APoint(a+l/2-250,d/2+z)
                ptext_6=APoint(a+l/2+250,d/2+z)
                line3=acad.model.AddLine(ptext_5,ptext_6)
                line3.layer='strrp'
                
                for j in range(n_center):
                    sp=sp+spacing_center
                    #print(sp)
                    p3=APoint(a+sp,z+cc)
                    p4=APoint(a+sp,z+d-cc)
                    line=acad.model.AddLine(p3,p4)
                    line.layer='Stirrups_center'         
            

        else:
                n_right=round(((l/3-50*2)/spacing_right))+1
                
                 ##Annotation
                ##inclined line
                ptext_1=APoint(a+5*l/6,d/2+z)
                ptext_2=APoint(a+5*l/6-46.6,-86.4+z)
                #Line1
                line1=acad.model.AddLine(ptext_1,ptext_2)
                line1.layer='text'
                ##Flat line
                ptext_3=APoint(a+5*l/6-46.6,-86.4+z)
                ptext_4=APoint(a+5*l/6-46.6-77,-86.4+z)
                ptext_5=APoint(a+5*l/6-46.6-77-468,-86.4+z)
                line2=acad.model.AddLine(ptext_3,ptext_4)
                line2.layer='text'
                ##Text To beshown
                text_dim=[n_right,stirrup_dia,spacing_right]
                text_length=acad.model.AddText(' %s-%smmdia@%smm c/c'%(text_dim[0],text_dim[1],text_dim[2]),ptext_5,25)
                text_length.layer='text'

                
                ##Stirrup lines @middle
                ptext_5=APoint(a+5*l/6-250,d/2+z)
                ptext_6=APoint(a+5*l/6+250,d/2+z)
                line3=acad.model.AddLine(ptext_5,ptext_6)
                line3.layer='strrp'
                
                
                for j in range(n_right):
                    sp=sp+spacing_right
                   # print(sp)
                    if sp>l-50:
                        sp=sp-50
                        #print(sp)
                        #p3=APoint(sp,cc)
                        #p4=APoint(sp,d-cc)
                        #line=acad.model.Addline(p3,p4)
                        #line.layer='Stirrups_sides'
                        break
                    p3=APoint(a+sp,z+cc)
                    p4=APoint(a+sp,z+d-cc)
                    line=acad.model.AddLine(p3,p4)
                    line.layer='Stirrups_sides' 

##For Section Details....
#1.Section A-A
def section_draw_AA(l_next,z,d,beam_cc,b,a):
    l=l_next
    cc=beam_cc
    left_cut=l/6
    center_cut=l/2
    right_cut=l/2+l/3

    section_cutx1=[a+left_cut,a+center_cut,a+right_cut]
    section_cuty1=[-300,-300,-300]

    section_cutx2=[a+left_cut,a+center_cut,a+right_cut]
    section_cuty2=[b+300,b+300,b+300]

    text=['A','B','C'] #####

    for j in range(len(section_cutx1)):
            Cut_line1=APoint(section_cutx1[j],section_cuty1[j]+z)
            text1=acad.model.AddText(' %s'%text[j],Cut_line1,50)
            text1.layer='text'
            Cut_line2=APoint(section_cutx2[j],section_cuty2[j]+z)
            text2=acad.model.AddText(' %s'%text[j],Cut_line2,50)
            text2.layer='text'
            line1=acad.model.AddLine(Cut_line1,Cut_line2)
            line1.layer='Section_line'
            
    ###Cross Sections
##Section AA
    p5x=[a+l/6-(b/2),a+l/6-(b/2),a+l/6+(b/2),a+l/6-(b/2),a+l/6-(b/2)+cc,a+l/6-(b/2)+cc,a+l/6+(b/2)-cc,a+l/6-(b/2)+cc,a+l/6-(b/2)+cc+20,a+l/6-(b/2)+cc]
    p5y=[-600,-(600+d),-600,-600,-600-cc,-(600+d)+cc,-600-cc,-600-cc,-600-cc,-600-cc-20]

    p6x=[a+l/6-(b/2),a+l/6+(b/2),a+l/6+(b/2),a+l/6+(b/2),a+l/6-(b/2)+cc,a+l/6+(b/2)-cc,a+l/6+(b/2)-cc,a+l/6+(b/2)-cc,a+l/6-(b/2)+cc+43,a+l/6-(b/2)+cc+23]
    p6y=[-(600+d),-(600+d),-(600+d),-600,-(600+d)+cc,-(600+d)+cc,-(600+d)+cc,-600-cc,-600-cc-23,-600-cc-43]

    for i in range(len(p5x)):
            Cut_line1=APoint(p5x[i],p5y[i]+z)
            #acad.model.AddText(' %s'%text[i],Cut_line1,50)
            Cut_line2=APoint(p6x[i],p6y[i]+z)
            #acad.model.AddText(' %s'%text[i],Cut_line2,50)
            line1=acad.model.AddLine(Cut_line1,Cut_line2)
            if i <=3:
                line1.layer='Beam_CSection'
            else:
                line1.layer='Stirrups_sides'
                
    ##Rebars    ##
    ##Need to manually enter these values
    no_rebar_lower=4
    no_rebar_upper=4
    dia_rebar_lower=10
    dia_rebar_upper=10
 
    ##Section__AA
    l=l_next
    cc=beam_cc
    v_interval=50
    text=['SECTION : A-A','SECTION : B-B','SECTION : C-C']
    for i in range(2):
          
                    if i==0:
                        ptext=APoint(a+l/6-b/2,-600-d-150+z)
                        text=acad.model.AddText(' %s'%text[i],ptext,30)
                        text.layer='text'
        ##Lower rebar   
                        #print('Section AA Lower: ')
                        #int(input('Corner Bar lower(mm) :'))
                        dia_rebar_lower_corner=16#int(input('Corner Bar lower(mm) :'))
                        sp=a+l/6-(b/2)+cc+dia_rebar_lower_corner
                        spacing=round(b-cc*2-2*dia_rebar_lower)/(no_rebar_lower-1)
                        for i in range(no_rebar_lower):
                            if i == 0:
                                p_center=APoint(sp,-(600+d)+cc+dia_rebar_lower_corner+z)
                                rebar1=acad.model.AddCircle(p_center,dia_rebar_lower_corner)
                                rebar1.layer='rebar_section'
                                
                                ##For annotation
                                ptext_4=APoint(a+l/6,z-600-d-72)
                                ptext_5=APoint(a+l/6+b/2+50,z-600-d-72)
                                line2=acad.model.AddLine(p_center,ptext_4)
                                line3=acad.model.AddLine(ptext_4,ptext_5)
                                text_dim=[dia_rebar_lower_corner]
                                text_length=acad.model.AddText(' %s mm dia'%(text_dim[0]),ptext_5,20)
                                
                                
                            elif i == no_rebar_lower-1:
                                p_center=APoint(a+l/6+(b/2)-cc-dia_rebar_lower_corner,-(600+d)+cc+dia_rebar_lower_corner+z)
                                rebar1=acad.model.AddCircle(p_center,dia_rebar_lower_corner)
                                rebar1.layer='rebar_section'
                                
                                ##For annotation
                                ptext_4=APoint(a+l/6,z-600-d-72)
                                #ptext_5=APoint(l/6+b/2+50,z-500-28)
                                line2=acad.model.AddLine(p_center,ptext_4)
                                #line3=acad.model.AddLine(ptext_4,ptext_5)
                                #text_dim=[dia_rebar_lower_corner]
                                #text_length=acad.model.AddText(' %s mm dia'%(text_dim[0]),ptext_5,20)
                                
                            else:
                                #print(sp)
                                sp=sp+spacing
                                #print(sp)
                                p_center=APoint(sp,-(600+d)+cc+dia_rebar_lower+z)
                                rebar1=acad.model.AddCircle(p_center,dia_rebar_lower)
                                rebar1.layer='rebar_section' 
                                
                                #Annotations
                                ptext_4=APoint(sp,-(600+d)+cc+dia_rebar_lower+z+v_interval)
                                ptext_5=APoint(a+l/6+b/2+50,-(600+d)+cc+dia_rebar_lower+z+v_interval)
                                line2=acad.model.AddLine(p_center,ptext_4)
                                line3=acad.model.AddLine(ptext_4,ptext_5)
                                
                                
                                text_dim=[dia_rebar_lower]
                                text_length=acad.model.AddText(' %s mm dia'%(text_dim[0]),ptext_5,20)
                                
                                #v_interval-=100

                    elif i==1:
                ##Upper rebar
                        #print('Section AA Upper: ')
                        dia_rebar_upper_corner=16#int(input('Corner Bar Upper(mm) :'))
                        sp=a+l/6-(b/2)+cc+dia_rebar_upper_corner
                        spacing=round(b-cc*2-dia_rebar_upper_corner*2)/(no_rebar_upper-1)
                        for i in range(no_rebar_upper):
                            if i == 0:
                                p_center=APoint(sp,-600-cc-dia_rebar_upper_corner+z)
                                rebar1=acad.model.AddCircle(p_center,dia_rebar_upper_corner)
                                rebar1.layer='rebar_section'
                                ##For annotation
                                ptext_4=APoint(a+l/6,z-500-28)
                                ptext_5=APoint(a+l/6+b/2+50,z-500-28)
                                line2=acad.model.AddLine(p_center,ptext_4)
                                line3=acad.model.AddLine(ptext_4,ptext_5)
                                text_dim=[dia_rebar_upper_corner]
                                text_length=acad.model.AddText(' %s mm dia'%(text_dim[0]),ptext_5,20)
                                
                            elif i == no_rebar_upper-1:
                                p_center=APoint(a+l/6+(b/2)-cc-dia_rebar_upper_corner,-600-cc-dia_rebar_upper_corner+z)
                                rebar1=acad.model.AddCircle(p_center,dia_rebar_upper_corner)
                                rebar1.layer='rebar_section'
                                ##For annotation
                                ptext_4=APoint(a+l/6,z-500-28)
                                #ptext_5=APoint(l/6+b/2+50,z-500-28)
                                line2=acad.model.AddLine(p_center,ptext_4)
                                #line3=acad.model.AddLine(ptext_4,ptext_5)
                                #text_dim=[dia_rebar_upper_corner]
                                #text_length=acad.model.AddText(' %s mm dia'%(text_dim[0]),ptext_5,20)
                                
                            else:
                                sp=sp+spacing
                                p_center=APoint(sp,-600-cc-dia_rebar_upper+z)
                                rebar1=acad.model.AddCircle(p_center,dia_rebar_upper)
                                rebar1.layer='rebar_section'
                                
                                #Annotations
                                ptext_4=APoint(sp,-600-cc-dia_rebar_upper+z-v_interval)
                                ptext_5=APoint(a+l/6+b/2+50,-600-cc-dia_rebar_upper+z-v_interval)
                                line2=acad.model.AddLine(p_center,ptext_4)
                                line3=acad.model.AddLine(ptext_4,ptext_5)
                                text_dim=[dia_rebar_upper]
                                text_length=acad.model.AddText(' %s mm dia'%(text_dim[0]),ptext_5,20)
                                
                                #v_interval-=100

##2.Section B-B

def section_draw_BB(l_next,z,d,beam_cc,b,a):
    ###Cross Sections
    l=l_next
    cc=beam_cc
    #left_cut=l/6
    center_cut=a+l/2
    v_interval=50
    right_cut=center_cut
##Section CC
    p5x=[right_cut-(b/2),right_cut-(b/2),right_cut+(b/2),right_cut-(b/2),right_cut-(b/2)+cc,right_cut-(b/2)+cc,right_cut+(b/2)-cc,right_cut-(b/2)+cc,right_cut-(b/2)+cc+20,right_cut-(b/2)+cc,]
    p5y=[-600,-(600+d),-600,-600,-600-cc,-(600+d)+cc,-600-cc,-600-cc,-600-cc,-600-cc-20]

    p6x=[right_cut-(b/2),right_cut+(b/2),right_cut+(b/2),right_cut+(b/2),right_cut-(b/2)+cc,right_cut+(b/2)-cc,right_cut+(b/2)-cc,right_cut+(b/2)-cc,right_cut-(b/2)+cc+43,right_cut-(b/2)+cc+23]
    p6y=[-(600+d),-(600+d),-(600+d),-600,-(600+d)+cc,-(600+d)+cc,-(600+d)+cc,-600-cc,-600-cc-23,-600-cc-43]

    for i in range(len(p5x)):
            Cut_line1=APoint(p5x[i],p5y[i]+z)
            #acad.model.AddText(' %s'%text[i],Cut_line1,50)
            Cut_line2=APoint(p6x[i],p6y[i]+z)
            #acad.model.AddText(' %s'%text[i],Cut_line2,50)
            line1=acad.model.AddLine(Cut_line1,Cut_line2)
            if i <=3:
                line1.layer='Beam_CSection'
            else:
                line1.layer='Stirrups_center'
    
##Rebars
    no_rebar_lower=3
    no_rebar_upper=3
    dia_rebar_lower=10
    dia_rebar_upper=10


##Section__CC
    text=['SECTION : B-B']
    for i in range(2):                          
            if i==0:
                        ptext=APoint(right_cut-b/2,-600-d-150+z)
                        text=acad.model.AddText(' %s'%text[i],ptext,30)
                        text.layer='text'                          
                          
##Lower rebar
                        #print('Section CC Lower: ')
                        dia_rebar_lower_corner=16#int(input('Corner Bar Lower(mm) :'))
                        sp=right_cut-(b/2)+cc+dia_rebar_lower_corner
                        spacing=round(b-cc*2-2*dia_rebar_lower_corner)/(no_rebar_lower-1)
                        for i in range(no_rebar_lower):
                            if i == 0:
                                p_center=APoint(sp,-(600+d)+cc+dia_rebar_lower_corner+z)
                                rebar1=acad.model.AddCircle(p_center,dia_rebar_lower_corner)
                                rebar1.layer='rebar_section'
                                
                                ##For annotation
                                ptext_4=APoint(a+l/2,z-600-d-72)
                                ptext_5=APoint(a+l/2+b/2+50,z-600-d-72)
                                line2=acad.model.AddLine(p_center,ptext_4)
                                line3=acad.model.AddLine(ptext_4,ptext_5)
                                text_dim=[dia_rebar_lower_corner]
                                text_length=acad.model.AddText(' %s mm dia'%(text_dim[0]),ptext_5,20)
                                
                            elif i == no_rebar_lower-1:
                                p_center=APoint(right_cut+(b/2)-cc-dia_rebar_lower_corner,-(600+d)+cc+dia_rebar_lower_corner+z)
                                rebar1=acad.model.AddCircle(p_center,dia_rebar_lower_corner)
                                rebar1.layer='rebar_section'
                                
                                ##For annotation
                                ptext_4=APoint(a+l/2,z-600-d-72)
                                #ptext_5=APoint(a+5*l/6+b/2+50,z-500-28)
                                line2=acad.model.AddLine(p_center,ptext_4)
                                #line3=acad.model.AddLine(ptext_4,ptext_5)
                                #text_dim=[dia_rebar_lower_corner]
                                #text_length=acad.model.AddText(' %s mm dia'%(text_dim[0]),ptext_5,20)
                                
                            else:
                                sp=sp+spacing
                                p_center=APoint(sp,-(600+d)+cc+dia_rebar_lower+z)
                                rebar1=acad.model.AddCircle(p_center,dia_rebar_lower)
                                rebar1.layer='rebar_section'     
                                
                                #Annotations
                                ptext_4=APoint(sp,-(600+d)+cc+dia_rebar_lower+z+v_interval) 
                                ptext_5=APoint(a+l/2+b/2+50,-(600+d)+cc+dia_rebar_lower+z+v_interval)
                                line2=acad.model.AddLine(p_center,ptext_4)
                                line3=acad.model.AddLine(ptext_4,ptext_5)
                                
                                
                                text_dim=[dia_rebar_lower]
                                text_length=acad.model.AddText(' %s mm dia'%(text_dim[0]),ptext_5,20)
                                
                                #v_interval-=100
                                
                                
            elif i==1:
                ##Upper rebar
                        #print('Section CC Upper: ')
                        dia_rebar_upper_corner=16#int(input('Corner Bar Upper(mm) :'))
                        
                        sp=right_cut-(b/2)+cc+dia_rebar_upper_corner
                        spacing=round(b-cc*2-2*dia_rebar_upper_corner)/(no_rebar_upper-1)
                        for i in range(no_rebar_upper):
                            if i == 0:
                                p_center=APoint(sp,-600-cc-dia_rebar_upper_corner+z)
                                rebar1=acad.model.AddCircle(p_center,dia_rebar_upper_corner)
                                rebar1.layer='rebar_section'
                                
                                ##For annotation
                                ptext_4=APoint(a+l/2,z-500-28)
                                ptext_5=APoint(a+l/2+b/2+50,z-500-28)
                                line2=acad.model.AddLine(p_center,ptext_4)
                                line3=acad.model.AddLine(ptext_4,ptext_5)
                                text_dim=[dia_rebar_upper_corner]
                                text_length=acad.model.AddText(' %s mm dia'%(text_dim[0]),ptext_5,20)
                                
                            elif i == no_rebar_upper-1:
                                p_center=APoint(right_cut+(b/2)-cc-dia_rebar_upper_corner,-600-cc-dia_rebar_upper_corner+z)
                                rebar1=acad.model.AddCircle(p_center,dia_rebar_upper_corner)
                                rebar1.layer='rebar_section'
                                
                                ##For annotation
                                ptext_4=APoint(a+l/2,z-500-28)
                                #ptext_5=APoint(a+5*l/6+b/2+50,z-500-28)
                                line2=acad.model.AddLine(p_center,ptext_4)
                                #line3=acad.model.AddLine(ptext_4,ptext_5)
                                #text_dim=[dia_rebar_lower_corner]
                                #text_length=acad.model.AddText(' %s mm dia'%(text_dim[0]),ptext_5,20)
                                
                            else:
                                sp=sp+spacing
                                p_center=APoint(sp,-600-cc-dia_rebar_upper+z)
                                rebar1=acad.model.AddCircle(p_center,dia_rebar_upper)
                                rebar1.layer='rebar_section'  
                                #Annotations
                                ptext_4=APoint(sp,-600-cc-dia_rebar_upper+z-v_interval)
                                ptext_5=APoint(a+l/2+b/2+50,-600-cc-dia_rebar_upper+z-v_interval)
                                line2=acad.model.AddLine(p_center,ptext_4)
                                line3=acad.model.AddLine(ptext_4,ptext_5)
                                text_dim=[dia_rebar_upper]
                                text_length=acad.model.AddText(' %s mm dia'%(text_dim[0]),ptext_5,20)
                                
                                #v_interval-=100

##3.Section C-C
def section_draw_CC(l_next,z,d,beam_cc,b,a):
    ###Cross Sections
    l=l_next
    cc=beam_cc
    #left_cut=l/6
    #center_cut=l/2
    v_interval=50
    right_cut=a+l/2+l/3
##Section CC
    p5x=[right_cut-(b/2),right_cut-(b/2),right_cut+(b/2),right_cut-(b/2),right_cut-(b/2)+cc,right_cut-(b/2)+cc,right_cut+(b/2)-cc,right_cut-(b/2)+cc,right_cut-(b/2)+cc+20,right_cut-(b/2)+cc,]
    p5y=[-600,-(600+d),-600,-600,-600-cc,-(600+d)+cc,-600-cc,-600-cc,-600-cc,-600-cc-20]

    p6x=[right_cut-(b/2),right_cut+(b/2),right_cut+(b/2),right_cut+(b/2),right_cut-(b/2)+cc,right_cut+(b/2)-cc,right_cut+(b/2)-cc,right_cut+(b/2)-cc,right_cut-(b/2)+cc+43,right_cut-(b/2)+cc+23]
    p6y=[-(600+d),-(600+d),-(600+d),-600,-(600+d)+cc,-(600+d)+cc,-(600+d)+cc,-600-cc,-600-cc-23,-600-cc-43]

    for i in range(len(p5x)):
            Cut_line1=APoint(p5x[i],p5y[i]+z)
            #acad.model.AddText(' %s'%text[i],Cut_line1,50)
            Cut_line2=APoint(p6x[i],p6y[i]+z)
            #acad.model.AddText(' %s'%text[i],Cut_line2,50)
            line1=acad.model.AddLine(Cut_line1,Cut_line2)
            if i <=3:
                line1.layer='Beam_CSection'
            else:
                line1.layer='Stirrups_sides'
    
##Rebars
    no_rebar_lower=4
    no_rebar_upper=4
    dia_rebar_lower=10
    dia_rebar_upper=10


##Section__CC
    text=['SECTION : C-C']
    for i in range(2):                          
            if i==0:
                        ptext=APoint(right_cut-b/2,-600-d-150+z)
                        text=acad.model.AddText(' %s'%text[i],ptext,30)
                        text.layer='text'                          
                          
##Lower rebar
                        #print('Section CC Lower: ')
                        dia_rebar_lower_corner=16#int(input('Corner Bar Lower(mm) :'))
                        sp=right_cut-(b/2)+cc+dia_rebar_lower_corner
                        spacing=round(b-cc*2-2*dia_rebar_lower_corner)/(no_rebar_lower-1)
                        for i in range(no_rebar_lower):
                            if i == 0:
                                p_center=APoint(sp,-(600+d)+cc+dia_rebar_lower_corner+z)
                                rebar1=acad.model.AddCircle(p_center,dia_rebar_lower_corner)
                                rebar1.layer='rebar_section'
                                
                                ##For annotation
                                ptext_4=APoint(a+5*l/6,z-600-d-72)
                                ptext_5=APoint(a+5*l/6+b/2+50,z-600-d-72)
                                line2=acad.model.AddLine(p_center,ptext_4)
                                line3=acad.model.AddLine(ptext_4,ptext_5)
                                text_dim=[dia_rebar_lower_corner]
                                text_length=acad.model.AddText(' %s mm dia'%(text_dim[0]),ptext_5,20)
                                
                            elif i == no_rebar_lower-1:
                                p_center=APoint(right_cut+(b/2)-cc-dia_rebar_lower_corner,-(600+d)+cc+dia_rebar_lower_corner+z)
                                rebar1=acad.model.AddCircle(p_center,dia_rebar_lower_corner)
                                rebar1.layer='rebar_section'
                                
                                ##For annotation
                                ptext_4=APoint(a+5*l/6,z-600-d-72)
                                #ptext_5=APoint(a+5*l/6+b/2+50,z-500-28)
                                line2=acad.model.AddLine(p_center,ptext_4)
                                #line3=acad.model.AddLine(ptext_4,ptext_5)
                                #text_dim=[dia_rebar_lower_corner]
                                #text_length=acad.model.AddText(' %s mm dia'%(text_dim[0]),ptext_5,20)
                                
                            else:
                                sp=sp+spacing
                                p_center=APoint(sp,-(600+d)+cc+dia_rebar_lower+z)
                                rebar1=acad.model.AddCircle(p_center,dia_rebar_lower)
                                rebar1.layer='rebar_section'     
                                
                                #Annotations
                                ptext_4=APoint(sp,-(600+d)+cc+dia_rebar_lower+z+v_interval)
                                ptext_5=APoint(a+5*l/6+b/2+50,-(600+d)+cc+dia_rebar_lower+z+v_interval)
                                line2=acad.model.AddLine(p_center,ptext_4)
                                line3=acad.model.AddLine(ptext_4,ptext_5)
                                
                                
                                text_dim=[dia_rebar_lower]
                                text_length=acad.model.AddText(' %s mm dia'%(text_dim[0]),ptext_5,20)
                                
                                #v_interval-=100
                                
                          
            elif i==1:
                ##Upper rebar
                        #print('Section CC Upper: ')
                        dia_rebar_upper_corner=16#int(input('Corner Bar Upper(mm) :'))
                        sp=right_cut-(b/2)+cc+dia_rebar_upper_corner
                        spacing=round(b-cc*2-2*dia_rebar_upper_corner)/(no_rebar_upper-1)
                        for i in range(no_rebar_upper):
                            if i == 0:
                                p_center=APoint(sp,-600-cc-dia_rebar_upper_corner+z)
                                rebar1=acad.model.AddCircle(p_center,dia_rebar_upper_corner)
                                rebar1.layer='rebar_section'
                                
                                ##For annotation
                                ptext_4=APoint(a+5*l/6,z-500-28)
                                ptext_5=APoint(a+5*l/6+b/2+50,z-500-28)
                                line2=acad.model.AddLine(p_center,ptext_4)
                                line3=acad.model.AddLine(ptext_4,ptext_5)
                                text_dim=[dia_rebar_upper_corner]
                                text_length=acad.model.AddText(' %s mm dia'%(text_dim[0]),ptext_5,20)
                                
                            elif i == no_rebar_upper-1:
                                p_center=APoint(right_cut+(b/2)-cc-dia_rebar_upper_corner,-600-cc-dia_rebar_upper_corner+z)
                                rebar1=acad.model.AddCircle(p_center,dia_rebar_upper_corner)
                                rebar1.layer='rebar_section'
                                
                                ##For annotation
                                ptext_4=APoint(a+5*l/6,z-500-28)
                                #ptext_5=APoint(a+5*l/6+b/2+50,z-500-28)
                                line2=acad.model.AddLine(p_center,ptext_4)
                                #line3=acad.model.AddLine(ptext_4,ptext_5)
                                #text_dim=[dia_rebar_lower_corner]
                                #text_length=acad.model.AddText(' %s mm dia'%(text_dim[0]),ptext_5,20)
                                
                            else:
                                sp=sp+spacing
                                p_center=APoint(sp,-600-cc-dia_rebar_upper+z)
                                rebar1=acad.model.AddCircle(p_center,dia_rebar_upper)
                                rebar1.layer='rebar_section'  
                                #Annotations
                                ptext_4=APoint(sp,-600-cc-dia_rebar_upper+z-v_interval)
                                ptext_5=APoint(a+5*l/6+b/2+50,-600-cc-dia_rebar_upper+z-v_interval)
                                line2=acad.model.AddLine(p_center,ptext_4)
                                line3=acad.model.AddLine(ptext_4,ptext_5)
                                text_dim=[dia_rebar_upper]
                                text_length=acad.model.AddText(' %s mm dia'%(text_dim[0]),ptext_5,20)
                                
                                #v_interval-=100

##For Final Output....
###Output @ Autocad
for i in range(N):
    beam_cc=20
    column_cc=40
    
    print('')
    print('Storey no {} :'.format(i))
    print('')
    
    span_no = int(input('Enter the no of span : '))
    a=int(input('Enter starting grid(mm) origin or shift from origin on right : '))   ## put span+no*width of column
    
    print('')
    
    a_initial=a
    
    
    l_initial = 0
    l_next = 0
    z1=0
    storey_height=3000##int(input('Enter the floor height(mm): '))    ###clear floor height
    for i in range(0,span_no):
        
      ##Parameters input
        print('***********************************************************')
        print('')
        l=int(input('Enter Beam Span(mm) no {} : '.format(i+1)))
        l_next=l
        b=300#int(input('Enter breadth(mm) : '))
        d=400#int(input('Enter depth(mm) : '))
        column_width=300#int(input('Enter the column width(mm) : '))
        print('')
        l_initial=a+l
        l=l_initial
        
        
        long_dim_x0 = [a,a,a,a+l_next,a+l_next,a+l_next/6-b/2,a+l_next/6-b/2,a+l_next/6-b/2,a+l_next/6+b/2,a+l_next/6+b/2,a+l_next/6-b/2-90,a+l_next/6-b/2-90,a+l_next/6-b/2-90,a+l_next/6-b/2-90,a+l_next/6-b/2-90]
        long_dim_y0 = [d+420,d+420,d+420,d+420,d+420,-460+z1,-460+z1,-460+z1,-460+z1,-460+z1,-600+z1,-600+z1,-600+z1,-600+z1-d,-600+z1-d]
        long_dim_x1 = [a+l_next,a+35.36,a+35.36,a+l_next-35.36,a+l_next-35.36,a+l_next/6+b/2,a+l_next/6-b/2+27.36,a+l_next/6-b/2+27.36,a+l_next/6+b/2-27.36,a+l_next/6+b/2-27.36,a+l_next/6-b/2-90,a+l_next/6-b/2-90-27.36,a+l_next/6-b/2-90+27.36,a+l_next/6-b/2-90-27.36,a+l_next/6-b/2-90+27.36]
        long_dim_y1 = [d+420,d+420+35.36,d+420-35.36,d+420+35.36,d+420-35.36,-460+z1,-460+z1+27.36,-460+z1-27.36,-460+z1+27.36,-460+z1-27.36,-600+z1-d,-600+z1-27.36,-600+z1-27.36,-600+z1+27.36-d,-600+z1+27.36-d]
        
        if span_no == 1:
            
            ###--------beam concrete longitudinal section ---------------------------------------###---------extra rebar------###                                                      ###l dimension of beam with arrow##
            p1x=[a-column_width,a,a,a+l_next,a+l_next+column_width,a-column_width,a-column_width,a+0,a+0,l_next+a,a+l_next+column_width,a+l_next/3,a+l_next/3,a+(l_next-(l_next/3)),a+(l_next-(l_next/3))]
            p1y=[0,0,0,0,d,d,d,d,d,d,d,d-beam_cc,beam_cc,beam_cc,d-beam_cc]

            p2x=[a-column_width,a,a+l_next,a+l_next,a+l_next+column_width,a-column_width,a-column_width,a+0,a+l_next,a+l_next,a+l_next+column_width,a+l_next/3+40,a+l_next/3+40,a+(l_next-(l_next/3))-40,a+(l_next-(l_next/3))-40]
            p2y=[-(d+200),-(d+200),0,-(d+200),-(d+200),d*2+200,-d,d*2+200,d,2*d+200,2*d+200,d-beam_cc-40,beam_cc+40,beam_cc+40,d-beam_cc-40]


            drawing=draw(p1x,p1y,p2x,p2y)
            draw_stirrup=stirrup(l_next,z,d,beam_cc,a)
            draw_section_AA=section_draw_AA(l_next,z,d,beam_cc,b,a)
            draw_section_BB=section_draw_BB(l_next,z,d,beam_cc,b,a)
            draw_section_CC=section_draw_CC(l_next,z,d,beam_cc,b,a)
            draw_l_dim=l_dimdraw(long_dim_x0,long_dim_y0,long_dim_x1,long_dim_y1)



            text_dim=[l_next,b,d]
            ptext_length=APoint(a+l_next/2-b/4,d+460+z)
            ptext_width=APoint(a+l_next/6-b/4,-430+z)
            ptext_depth=APoint(a+l_next/6-b-100,z-600-d/2)

            text_length=acad.model.AddText(' %s'%text_dim[0],ptext_length,30)
            text_length.layer='text'

            text_width=acad.model.AddText(' %s'%text_dim[1],ptext_width,30)
            text_width.layer='text'

            text_depth=acad.model.AddText(' %s'%text_dim[2],ptext_depth,30)
            text_depth.layer='text'

        else:
        
        
            if i == 0 :

                    ###--------beam concrete longitudinal section ---------------------------------------###---------extra rebar------###                                                      ###l dimension of beam with arrow##
                    p1x=[a-column_width,a,a,a+l_next,a+l_next+column_width,a-column_width,a-column_width,a+0,a+0,l_next+a,a+l_next+column_width,a+l_next/3,a+l_next/3,a+(l_next-(l_next/3)),a+(l_next-(l_next/3))]
                    p1y=[0,0,0,0,0,d,d,d,d,d,d,d-beam_cc,beam_cc,beam_cc,d-beam_cc]

                    p2x=[a-column_width,a,a+l_next,a+l_next,a+l_next+column_width,a-column_width,a-column_width,a+0,a+l_next,a+l_next,a+l_next+column_width,a+l_next/3+40,a+l_next/3+40,a+(l_next-(l_next/3))-40,a+(l_next-(l_next/3))-40]
                    p2y=[-(d+200),-(d+200),0,-(d+200),-(d+200),d*2+200,-d,d*2+200,d,2*d+200,2*d+200,d-beam_cc-40,beam_cc+40,beam_cc+40,d-beam_cc-40]


                    drawing=draw(p1x,p1y,p2x,p2y)
                    draw_stirrup=stirrup(l_next,z,d,beam_cc,a)
                    draw_section_AA=section_draw_AA(l_next,z,d,beam_cc,b,a)
                    draw_section_BB=section_draw_BB(l_next,z,d,beam_cc,b,a)
                    draw_section_CC=section_draw_CC(l_next,z,d,beam_cc,b,a)
                    draw_l_dim=l_dimdraw(long_dim_x0,long_dim_y0,long_dim_x1,long_dim_y1)


    

                    text_dim=[l_next,b,d]
                    ptext_length=APoint(a+l_next/2-b/4,d+460+z)
                    ptext_width=APoint(a+l_next/6-b/4,-430+z)
                    ptext_depth=APoint(a+l_next/6-b-100,z-600-d/2)

                    text_length=acad.model.AddText(' %s'%text_dim[0],ptext_length,30)
                    text_length.layer='text'

                    text_width=acad.model.AddText(' %s'%text_dim[1],ptext_width,30)
                    text_width.layer='text'

                    text_depth=acad.model.AddText(' %s'%text_dim[2],ptext_depth,30)
                    text_depth.layer='text'


            elif i == span_no-1:

                p1x=[a,a,l,l,l+column_width,a+l_next/3,a+l_next/3,a+(l_next-(l_next/3)),a+(l_next-(l_next/3))]
                p1y=[d,0,d,0,d*2+200,d-beam_cc,beam_cc,beam_cc,d-beam_cc]

                p2x=[l,l,l,l,l+column_width,a+l_next/3+40,a+l_next/3+40,a+(l_next-(l_next/3))-40,a+(l_next-(l_next/3))-40]
                p2y=[d,0,2*d+200,-(d+200),-(d+200),d-beam_cc-40,beam_cc+40,beam_cc+40,d-beam_cc-40]

                drawing=draw(p1x,p1y,p2x,p2y)
                draw_stirrup=stirrup(l_next,z,d,beam_cc,a)
                draw_section_AA=section_draw_AA(l_next,z,d,beam_cc,b,a)
                draw_section_BB=section_draw_BB(l_next,z,d,beam_cc,b,a)
                draw_section_CC=section_draw_CC(l_next,z,d,beam_cc,b,a)
                draw_l_dim=l_dimdraw(long_dim_x0,long_dim_y0,long_dim_x1,long_dim_y1)

                text_dim=[l_next,b,d]
                ptext_length=APoint(a+l_next/2-b/4,d+460+z)
                ptext_width=APoint(a+l_next/6-b/4,-430+z)
                ptext_depth=APoint(a+l_next/6-b-100,z-600-d/2)

                text_length=acad.model.AddText(' %s'%text_dim[0],ptext_length,30)
                text_length.layer='text'

                text_width=acad.model.AddText(' %s'%text_dim[1],ptext_width,30)
                text_width.layer='text'

                text_depth=acad.model.AddText(' %s'%text_dim[2],ptext_depth,30)
                text_depth.layer='text'


            else:
                p1x=[a,a,l,l,l+column_width,l+column_width,a+l_next/3,a+l_next/3,a+(l_next-(l_next/3)),a+(l_next-(l_next/3))]
                p1y=[d,0,d,0,d,0,d-beam_cc,beam_cc,beam_cc,d-beam_cc]

                p2x=[l,l,l,l,l+column_width,l+column_width,a+l_next/3+40,a+l_next/3+40,a+(l_next-(l_next/3))-40,a+(l_next-(l_next/3))-40]
                p2y=[d,0,2*d+200,-(d+200),(d*2+200),-(d+200),d-beam_cc-40,beam_cc+40,beam_cc+40,d-beam_cc-40]

                drawing_1=draw(p1x,p1y,p2x,p2y)
                draw_stirrup=stirrup(l_next,z,d,beam_cc,a)
                draw_section_AA=section_draw_AA(l_next,z,d,beam_cc,b,a)
                draw_section_BB=section_draw_BB(l_next,z,d,beam_cc,b,a)
                draw_section_CC=section_draw_CC(l_next,z,d,beam_cc,b,a)
                draw_l_dim=l_dimdraw(long_dim_x0,long_dim_y0,long_dim_x1,long_dim_y1)


                text_dim=[l_next,b,d]
                ptext_length=APoint(a+l_next/2-b/4,d+460+z)
                ptext_width=APoint(a+l_next/6-b/4,-430+z)
                ptext_depth=APoint(a+l_next/6-b-100,z-600-d/2)

                text_length=acad.model.AddText(' %s'%text_dim[0],ptext_length,30)
                text_length.layer='text'

                text_width=acad.model.AddText(' %s'%text_dim[1],ptext_width,30)
                text_width.layer='text'

                text_depth=acad.model.AddText(' %s'%text_dim[2],ptext_depth,30)
                text_depth.layer='text'
            
            
            
        a=l_initial+column_width

        l_initial=l_initial+column_width

        dimension_each=a-l
        #print(l,a)
        #print(dimension_each)
   

    draw_without_cantilever(column_width,column_cc,a,a_initial,d,beam_cc)
    
    
    
    
    z=z+storey_height+d
    z1=z-storey_height-d
    

print('')
print('****************************************************')
print('')
print("Drawing has been created....")
print('')
print('****************************************************')
