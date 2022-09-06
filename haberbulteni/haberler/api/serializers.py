from rest_framework import serializers
from haberler.models import Makale,Gazeteci
from datetime import datetime
from datetime import date
from django.utils.timesince import timesince

class MakaleSerializer(serializers.ModelSerializer):   
    time_since_pub = serializers.SerializerMethodField()
    #yazar = serializers.StringRelatedField()
    # yazar = GazeteciSerializer()
    class Meta:
        model = Makale
        fields = '__all__'
        #fields = ['yazar','baslik','metin']

    def get_time_since_pub(self,object):
        now = datetime.now()
        pub_date = object.yayımlanma_tarihi
        if object.aktif == True:
            time_delta = timesince(pub_date,now)
            return time_delta
        else:
            return 'Aktif degil'
        
    def validate_yayimlanma_tarihi(value,tarih):
        today = date.today()
        if tarih > today:
            raise serializers.ValidationError('Yayimlanma tarihi ileri bir tarih olamaz!!')
        return tarih


class GazeteciSerializer(serializers.ModelSerializer):
    # makaleler = MakaleSerializer(many=True,read_only=True)
    makaleler = serializers.HyperlinkedRelatedField(many=True,read_only=True,view_name='makale-detay')

    class Meta:
        model = Gazeteci
        fields = '__all__'




#Standard serializer
class MakaleDefaultSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    yazar = serializers.CharField()
    baslik = serializers.CharField()
    aciklama = serializers.CharField()
    metin = serializers.CharField()
    sehir = serializers.CharField()
    yayımlanma_tarihi = serializers.DateField()
    aktif = serializers.BooleanField()
    yaratilma_tarihi = serializers.DateTimeField(read_only=True)
    güncelleneme_tarihi = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        print(validated_data)
        return Makale.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.yazar = validated_data.get('yazar',instance.yazar)
        instance.baslik = validated_data.get('baslik',instance.baslik)
        instance.aciklama = validated_data.get('aciklama',instance.aciklama)
        instance.metin = validated_data.get('metin',instance.metin)
        instance.sehir = validated_data.get('sehir',instance.sehir)
        instance.yayımlanma_tarihi = validated_data.get('yayımlanma_tarihi',instance.yayımlanma_tarihi)
        instance.aktif = validated_data.get('aktif',instance.aktif)
        instance.save()
        return instance


    def validate(self, data): #object level >> dönen datayı check eder
        if data['baslik'] == data['aciklama']:
            raise serializers.ValidationError('Baslik ve aciklama alanları farklı olmalıdır. Lutfen farkli aciklama giriniz')
        return data


    def validate_baslik(self,value):
        if len(value)<20:
            raise serializers.ValidationError(f'Baslik alani minimum 20 karakter olmali, siz {len(value)} karakter girdiniz!')
        return value
