import pandas
import math
import pytz
from .models import * 


def datascrapping():
    df = pandas.read_excel("/home/amit/Downloads/evaluation_register_RAIPUR.xlsx", sheetname='AUG 2018')
    exceldata = df.to_dict(orient='records')
    mldata = {'E-Class':25000,'A Class':17500,'CLA Class':17500,'GLA Class':17500,'B-Class':12500, 'C-Class':20000}
    for i in exceldata:
        eval_date = evaldateclean(i['Date'])
        print("DATAPASSEDBY FUnction",i['Make'],i['Model'])
        model = identifymodel(i['Make'],i['Model'])
        variant = identifyvariant(i['Make'],i['Model'])
        make = identifymake(i['Make'],i['Model'])
        print("DATA rETurn",model)
        print("erv",i['Price offered'])
        if variant and model:
            eval_date = eval_date.replace(tzinfo=pytz.UTC)
            i['created'] = eval_date
            i['Kms Driven'] = i['Kilometers']
            i['Make'] = make.name
            i['Model'] = model.name
            i['Variant'] = variant.name
            i['MFG Year'] = i['Y.O.M']
            print(i)
            i['Trade-In Price'] = i['Price offered']
            car_already_exists = UsedCarDetail.objects.filter(source__name="Autohangar", year__name=int(i['Y.O.M']),model=model,make=make,variant=variant)      
            print(car_already_exists)
            if not car_already_exists:
                print("CAR NOT Existed Already")
                create_used_car(i,mldata)
            else:
                print("CAR Existed")
                print(eval_date,"jj",car_already_exists[0].created_on)
                if (eval_date >= car_already_exists[0].created_on):
                    print("wekrjn")
                    delete_old_used_car(i)
                    create_used_car(i,mldata)
        else:
            pass
from datetime import datetime 


makename = {'MERC':'Mercedes-Benz'}




def evaldateclean(date):
    print("DDF",date)
    try:
        return date.to_pydatetime()
    except Exception as e:
        eval_date=datetime.strptime(date, '%d/%m/%Y')
        # if eval_date.month > 1:
        #     eval_date=datetime.strptime(date, '%m/%d/%Y')
        #     return eval_date
        return eval_date


def identifymodel(make, model):
    if make in makename:
        make = makename[make]
    makefil = Make.objects.filter(name__icontains=make)
    if makefil:
        modeldata = model.split(' ')
        modelfil = Model.objects.filter(make=makefil[0], name=modeldata[0])
        if modelfil:
            variantfil = Variant.objects.filter(make=makefil[0], name__in=modeldata[1:])
            if variantfil:
                print(makefil[0], modelfil[0], variantfil[0])
                return modelfil[0]
        else:
            modelfil = Model.objects.filter(make=makefil[0], name=modeldata[0][0]+"-Class") 
            variantfil = Variant.objects.filter(make=makefil[0], name__icontains=model)
            if modelfil:
                if variantfil:
                    print(makefil[0], modelfil[0], variantfil[0])
                    return modelfil[0]  

def identifyvariant(make,model):
    if make in makename:
        make = makename[make]
    makefil = Make.objects.filter(name__icontains=make)
    if makefil:
        modeldata = model.split(' ')
        modelfil = Model.objects.filter(make=makefil[0], name=modeldata[0])
        if modelfil:
            variantfil = Variant.objects.filter(make=makefil[0], name__in=modeldata[1:])
            if variantfil:
                print(makefil[0], modelfil[0], variantfil[0])
                return variantfil[0]
        else:
            modelfil = Model.objects.filter(make=makefil[0], name=modeldata[0][0]+"-Class") 
            variantfil = Variant.objects.filter(make=makefil[0], name__icontains=model)
            if variantfil:
                return variantfil[0] 



def identifymake(make, model):
    if make in makename:
        make = makename[make]
    makefil = Make.objects.filter(name__icontains=make)
    if makefil:
        modeldata = model.split(' ')
        modelfil = Model.objects.filter(make=makefil[0], name=modeldata[0])
        if modelfil:
            variantfil = Variant.objects.filter(make=makefil[0], name__in=modeldata[1:])
            if variantfil:
                print(makefil[0], modelfil[0], variantfil[0])
                return makefil[0]
        else:
            modelfil = Model.objects.filter(make=makefil[0], name=modeldata[0][0]+"-Class") 
            variantfil = Variant.objects.filter(make=makefil[0], name__icontains=model)
            if variantfil:
                print(makefil[0])
                return makefil[0]









    # model = Model.objects.get(name=model)

# for i in exceldata:
#     p=float(i['Trade-In Price'])
#     d = math.isnan(p)
#     print(float(i['Trade-In Price']))
#     print(d)
#     if d == False:
#         eval_date=datetime.strptime(i['Evaluation Date'], '%Y-%m-%d')
#         eval_date = eval_date.replace(tzinfo=pytz.UTC)
#         i['created'] = eval_date
#         print(i)
#         car_already_exists = UsedCarDetail.objects.filter(source__name="Autohangar", year__name=int(i['MFG Year']),model__name=i['Model'],make__name=i['Make'],variant__name=i['Variant'])      
#         print(car_already_exists)
#         if not car_already_exists:
#             print("CAR NOT Existed Already")
#             create_used_car(i,mldata)
#         else:
#             print("CAR Existed")
#             print(eval_date,"jj",car_already_exists[0].created_on)
#             if (eval_date >= car_already_exists[0].created_on):
#                 print("wekrjn")
#                 delete_old_used_car(i)
#                 create_used_car(i,mldata)

def  delete_old_used_car(i):
    UsedCarDetail.objects.filter(source__name="Autohangar", make__name=i['Make'], model__name=i['Model'], variant__name=i['Variant']).delete()
    
def create_used_car(i,mldata):
    print("ousrj")
    source = Source.objects.get(name="Autohangar")
    year = Year.objects.get(name=int(i['MFG Year']))
    model = Model.objects.get(name=i['Model'])
    make = Make.objects.get(name=i['Make'])
    variant = Variant.objects.get(name=i['Variant'])
    no_of_user = NoOfUser.objects.get(number=1)
    km = KilometersDriven.objects.get(from_kms__lt=i['Kms Driven'],to_kms__gte=i['Kms Driven'])
    cardekho_car= UsedCarDetail.objects.filter(source__name="Cardekho", year=year,model__name=model,make__name=make,variant=variant,kms_driven=km,no_of_users=no_of_user).first()
    kmrange = KilometersDriven.objects.exclude(id=km.id)
    print("CARDEKHO", cardekho_car)
    if cardekho_car:
        new_car= UsedCarDetail.objects.create(source=source, year=year,model=model,make=make,variant=variant,kms_driven=km,no_of_users=no_of_user,fair_from_price=getprice(i['Trade-In Price'], 15, "decrement"),fair_to_price=getprice(i['Trade-In Price'], 10, "decrement"),good_from_price=getprice(i['Trade-In Price'], 5,"decrement"),good_to_price=getprice(i['Trade-In Price'], 0,None),excellent_from_price=getprice(i['Trade-In Price'], 5, "increment"),excellent_to_price=getprice(i['Trade-In Price'], 10, "increment"), created_on=i['created'])            
        for kms in kmrange:
            print("CAR DATA FROM CAR DEKHO")
            kmcardekho_car = UsedCarDetail.objects.filter(source__name="Cardekho", year=year,model__name=model,make__name=make,variant=variant,kms_driven=kms,no_of_users=no_of_user).first()
            used_car = UsedCarDetail.objects.create(source=source, year=year,model=model,make=make,variant=variant,kms_driven=kms,no_of_users=no_of_user,fair_from_price=calculateratio(new_car.fair_from_price,cardekho_car.fair_from_price,kmcardekho_car.fair_from_price),fair_to_price=calculateratio(new_car.fair_to_price,cardekho_car.fair_to_price,kmcardekho_car.fair_to_price),good_from_price=calculateratio(new_car.good_from_price,cardekho_car.good_from_price,kmcardekho_car.good_from_price),good_to_price=calculateratio(new_car.good_to_price,cardekho_car.good_to_price,kmcardekho_car.good_to_price),excellent_from_price=calculateratio(new_car.excellent_from_price,cardekho_car.excellent_from_price,kmcardekho_car.excellent_from_price),excellent_to_price=calculateratio(new_car.excellent_to_price,cardekho_car.excellent_to_price,kmcardekho_car.excellent_to_price), created_on=i['created'])        
            print("sdsd",kms,used_car.good_to_price,kmcardekho_car.good_to_price,new_car.good_to_price,cardekho_car.good_to_price)
    
    else:
        print("KIKI")
        if model.name in mldata:
            print("sd")
            kmonwards = KilometersDriven.objects.filter(to_kms__gte=i['Kms Driven'])
            car_price = i['Trade-In Price']
            dummyvar = 0
            km_car_price = car_price
            for kms in kmonwards:
                km_car_price = km_car_price - dummyvar
                dummyvar = mldata[model.name]
                print("PRICE", km_car_price)
                print("KMOnward",kms,km_car_price)
                used_car = UsedCarDetail.objects.create(source=source, year=year,model=model,make=make,variant=variant,kms_driven=kms,no_of_users=no_of_user,fair_from_price=getprice(km_car_price, 15, "decrement"),fair_to_price=getprice(km_car_price, 10, "decrement"),good_from_price=getprice(km_car_price, 5,"decrement"),good_to_price=getprice(km_car_price,0,None),excellent_from_price=getprice(km_car_price, 5,"increment"),excellent_to_price=getprice(km_car_price, 10, "increment"), created_on=i['created'])        
                print(used_car.id)            
            kmbackwards = KilometersDriven.objects.filter(to_kms__lt=i['Kms Driven']).order_by('-id')
            backword_car_price = car_price
            for kms in kmbackwards:
                backword_car_price = backword_car_price + mldata[model.name]
                print("BACK_PRICE", km_car_price)
                print("KMBACK",kms,backword_car_price)
                used_car = UsedCarDetail.objects.create(source=source, year=year,model=model,make=make,variant=variant,kms_driven=kms,no_of_users=no_of_user,fair_from_price=getprice(backword_car_price, 15,"decrement"),fair_to_price=getprice(backword_car_price, 10, "decrement"),good_from_price=getprice(backword_car_price, 5, "decrement"),good_to_price=getprice(backword_car_price, 1,None),excellent_from_price=getprice(backword_car_price, 5,"increment"),excellent_to_price=getprice(backword_car_price, 10,"increment"), created_on=i['created'])      
                print(used_car.id)
        else:
            new_car= UsedCarDetail.objects.create(source=source, year=year,model=model,make=make,variant=variant,kms_driven=km,no_of_users=no_of_user,fair_from_price=getprice(i['Trade-In Price'], 15, "decrement"),fair_to_price=getprice(i['Trade-In Price'], 10, "decrement"),good_from_price=getprice(i['Trade-In Price'], 5,"decrement"),good_to_price=getprice(i['Trade-In Price'], 0,None),excellent_from_price=getprice(i['Trade-In Price'], 5, "increment"),excellent_to_price=getprice(i['Trade-In Price'], 10, "increment"), created_on=i['created'])            



def calculateratio(autohangarprice,cardekhoprice,respectivecardekhoprice):
    return (cardekhoprice/autohangarprice)*respectivecardekhoprice
    

def getprice(price, changeperc, offsettype):
    if offsettype == "decrement":
        return int(price)-((int(price)/100)*changeperc)
    if offsettype == "increment":
        return int(price)+((int(price)/100)*changeperc)

    else:
        return int(price)
