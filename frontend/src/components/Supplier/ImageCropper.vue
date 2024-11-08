<script setup>
import { ref, watch, onMounted } from 'vue';
import { Cropper } from 'vue-advanced-cropper';
import 'vue-advanced-cropper/dist/style.css';

const props = defineProps({
    imageFile: {
    type: File,
    required: true
    }
});

const emit = defineEmits(['crop-complete', 'cancel']);

const cropperRef = ref(null);
const imageUrl = ref('');

// Create URL for the uploaded image
const createImageUrl = () => {
    console.log('Creating image URL for file:', props.imageFile); // Debug log
    if (props.imageFile) {
        imageUrl.value = URL.createObjectURL(props.imageFile);
        console.log('Created URL:', imageUrl.value); // Debug log
    }
};

// Function to get the cropped image
const crop = () => {
    console.log('Cropping image...'); // Debug log
    if (!cropperRef.value) {
        console.error('Cropper ref is null'); // Debug log
        return;
    }

const { coordinates, canvas } = cropperRef.value.getResult();

canvas.toBlob((blob) => {
    if (blob) {
        const croppedFile = new File([blob], props.imageFile.name, {
        type: 'image/jpeg',
        lastModified: Date.now(),
    });

emit('crop-complete', {
    file: croppedFile,
    coordinates,
            url: URL.createObjectURL(croppedFile)
        });
    }
    }, 'image/jpeg', 0.85);
};

const handleCancel = () => {
    emit('cancel');
};

// Create image URL immediately when component mounts
onMounted(() => {
    console.log('ImageCropper mounted'); // Debug log
    createImageUrl();
});

// Also watch for changes in the image file
watch(() => props.imageFile, () => {
    console.log('Image file changed'); // Debug log
    createImageUrl();
});
</script>

<template>
    <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white p-6 rounded-lg w-[90%] max-w-2xl">
            <div class="mb-4 flex justify-between items-center">
                <h3 class="text-lg font-semibold">Crop Image</h3>
                <button 
                    @click="handleCancel"
                    class="text-gray-500 hover:text-gray-700"
                >
                    ✕
                </button>
            </div>

            <!-- Debug info -->
            <div v-if="!imageUrl" class="text-red-500 mb-4">
                No image URL available
            </div>

            <div class="w-full h-[400px] border border-gray-200 rounded-lg overflow-hidden">
            <Cropper
                v-if="imageUrl"
                ref="cropperRef"
                :src="imageUrl"
                :stencil-props="{
                aspectRatio: 1
                }"
                class="h-full w-full"
                image-restriction="stencil"
                :default-boundaries="{ width: '100%', height: '100%' }"
                :default-size="{
                width: '80%',
                height: '80%'
                }"
            />
            </div>

            <div class="mt-4 flex justify-end gap-2">
            <button
                @click="handleCancel"
                class="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded-lg"
            >
                Cancel
            </button>
            <button
                @click="crop"
                class="px-4 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-lg"
            >
                Crop Image
            </button>
        </div>
    </div>
</div>
</template>