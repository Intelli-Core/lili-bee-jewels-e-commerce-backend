from rest_framework import serializers

from .models import (
    Product,
    ProductAttributes,
    ProductCategory,
    ProductImage,
    ProductOption,
)


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = "__all__"


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["image"]


class ProductAtrtributeSerializer(serializers.ModelSerializer):
    weight = serializers.FloatField()

    class Meta:
        model = ProductAttributes
        fields = "__all__"

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ProductOptionSerializer(serializers.ModelSerializer):
    attributes = ProductAtrtributeSerializer()
    price = serializers.FloatField()
    media = serializers.ListField(
        child=serializers.ImageField(), required=False, write_only=True
    )

    class Meta:
        model = ProductOption
        fields = "__all__"

    def create(self, validated_data):
        # Media
        media_data = validated_data.pop("media", [])

        # Attributes
        attributes_data = validated_data.pop("attributes")
        attributes = ProductAttributes.objects.create(**attributes_data)

        product_option = ProductOption.objects.create(
            attributes=attributes, **validated_data
        )

        for image in media_data:
            ProductImage.objects.create(
                product_option=product_option,
                product=product_option.product,
                image=image,
            )
        return product_option

    def update(self, instance, validated_data):
        # Thubnail
        thumbnail = validated_data.pop("thumbnail", None)
        if thumbnail is not None:
            instance.thumbnail = thumbnail

        # Media
        media_data = validated_data.pop("media", [])
        for image_data in media_data:
            ProductImage.objects.create(
                product=instance.product, image=image_data, product_option=instance
            )

        # Attributes
        attributes_data = validated_data.pop("attributes", None)
        if attributes_data:
            attributes_serializer = ProductAtrtributeSerializer(
                instance.attributes, data=attributes_data, partial=True
            )
            if attributes_serializer.is_valid():
                attributes_serializer.save()

        instance.save()
        return instance

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["media"] = ProductImageSerializer(instance.media.all(), many=True).data
        return response


class ProductSerializer(serializers.ModelSerializer):
    attributes = ProductAtrtributeSerializer(required=False)
    options = ProductOptionSerializer(many=True, read_only=True)
    price = serializers.FloatField(required=True)
    media = serializers.ListField(
        child=serializers.ImageField(), required=False, write_only=True
    )

    class Meta:
        model = Product
        fields = "__all__"

    def create(self, validated_data):
        # Media
        media_data = validated_data.pop("media", [])

        # Atributes
        attributes_data = validated_data.pop("attributes", None)
        attributes = (
            ProductAttributes.objects.create(**attributes_data)
            if attributes_data
            else None
        )
        product = Product.objects.create(attributes=attributes, **validated_data)

        for image in media_data:
            ProductImage.objects.create(product=product, image=image)
        return product

    def update(self, instance, validated_data):
        # Thubnail
        thumbnail = validated_data.pop("thumbnail", None)
        if thumbnail is not None:
            instance.thumbnail = thumbnail

        # Media
        media_data = validated_data.pop("media", [])
        for image_data in media_data:
            ProductImage.objects.create(product=instance, image=image_data)

        # Attributes
        attributes_data = validated_data.pop("attributes", None)
        if attributes_data:
            attributes_serializer = ProductAtrtributeSerializer(
                instance.attributes, data=attributes_data, partial=True
            )
            if attributes_serializer.is_valid():
                attributes_serializer.save()
        instance.save()
        return instance

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["category"] = ProductCategorySerializer(instance.category).data
        response["media"] = ProductImageSerializer(instance.media.all(), many=True).data
        for option in response["options"]:
            option.pop("product", None)
        return response
