import pandas
df = pandas.read_csv("C:/Users/User/Desktop/Priyanka_Workspace/Data Scrapping/Autohangar/evaluation_report (18).csv", usecols=['Evaluation Date','Make','Model','Variant','Kms Driven','MFG Year','Trade-In Price'])
exceldata = df.to_dict(orient='records')

mldata = {'E-Class':25000,'A Class':17500,'CLA Class':17500,'GLA Class':17500,'B-Class':12500, 'C-Class':20000}
for i in exceldata:
	if i.purchesprice:
        car_already_exists = UsedCarDetail.objects.filter(source__name="Autohangar", year__name=i.year,model__name=i.model,make__name=i.make,variant__name=i.variant)        
	    if not car_already_exists:
	        create_used_car():
	    else:
	        if i.evaluation_date > u.created_on :
	        	create_used_car()
	        	delete_old_used_car()

def  delete_old_used_car():
	UsedCarDetail.objects.filter(source__name="Autohangar", make__name=i.make, model__name=i.model, varient__name=i.varient).delete()
	
def create_used_car():
	source = Source.objects.get(name="Autohangar")
	year = Year.objects.get(name=i.year)
	model = Model.objects.get(name=i.model)
	make = Make.objects.get(name=i.make)
	varient = Varient.objects.get(name=i.varient)
	km = KilometersDriven.objects.get(from_kms__lt=i.kilo_driven,to_kms__gte=i.kilo_driven)
   	new_car= UsedCarDetail.objects.create(source=source, year=year,model__name=model,make__name=make,variant=variant,kms_driven=km,no_of_users=1,fair_from_price=getprice(i.purchesprice, -15),fair_to_price=getprice(i.purchesprice, -10),good_from_price=getprice(i.purchesprice,-5),good_to_price=getprice(i.purchesprice, 0),excellent_from_price=getprice(i.purchesprice, +5),excellent_to_price=getprice(i.purchesprice, +10), created_on=i.evaluation_date)            
    cardekho_car= UsedCarDetail.objects.filter(source__name="Cardekho", year=year,model__name=model,make__name=make,variant=variant,kms_driven=km,no_of_users=1)
    kmrange = KilometersDriven.objects.exclude(id=km.id)
    if cardekho_price:
	    for kms in kmrange:
	    	kmcardekho_car = UsedCarDetail.objects.filter(source="Cardekho", year=year,model__name=model,make__name=make,variant=variant,kms_driven=km,no_of_users=1)
	    	used_car = UsedCarDetail.objects.create(source=source, year=year,model__name=model,make__name=make,variant=variant,kms_driven=kms,no_of_users=1,fair_from_price=calculateratio(new_car.fair_from_price,cardekho_car.fair_from_price,kmcardekho_car.fair_from_price),fair_to_price=calculateratio(new_car.fair_to_price,cardekho_car.fair_to_price,kmcardekho_car.fair_to_price),good_from_price=calculateratio(new_car.good_from_price,cardekho_car.good_from_price,kmcardekho_car.good_from_price),good_to_price=calculateratio(new_car.good_to_price,cardekho_car.good_to_price,kmcardekho_car.good_to_price),excellent_from_price=calculateratio(new_car.excellent_from_price,cardekho_car.excellent_from_price,kmcardekho_car.excellent_from_price),excellent_to_price=calculateratio(new_car.excellent_to_price,cardekho_car.excellent_to_price,kmcardekho_car.excellent_to_price), created_on=i.evaluation_date)        
    else:
    	if model.name in mldata:
    		car_price = i.purchesprice - 
    		for kms in range(kmrange[0], ):
    			car_price = car_price + mldata[model.name]
    			if car_price == i.
		    	 used_car = UsedCarDetail.objects.create(source=source, year=year,model__name=model,make__name=make,variant=variant,kms_driven=kms,no_of_users=1,fair_from_price=getprice(car_price, -15),fair_to_price=getprice(car_price, -10),good_from_price=getprice(car_price, -5),good_to_price=getprice(car_price, 0),excellent_from_price=getprice(car_price, +5),excellent_to_price=getprice(car_price, +10), created_on=i.evaluation_date)        





def calculateratio(autohangarprice,cardekhoprice,respectivecardekhoprice):
	return (cardekhoprice/autohangarprice)+respectivecardekhoprice
	

def getprice(price, changeperc):
	return price/changeperc
