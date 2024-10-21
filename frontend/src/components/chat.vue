<template>
    <div class="flex flex-col h-screen p-4">
    <div v-if="isLoadingPartners" class="text-center">Loading partners...</div>
    <div v-else-if="!currentUser" class="text-center">Please log in to use the chat.</div>
    <div v-else class="h-full flex flex-col">
    <div v-if="!selectedPartner" class="w-full">
        <h2 class="text-xl font-bold mb-4">Select a {{ currentUser.userType === 'supplier' ? 'Restaurant' : 'Supplier' }} to chat with:</h2>
        <ul>
        <li v-for="partner in availablePartners" :key="partner.id" class="flex justify-between items-center p-2 mb-2 bg-gray-100 rounded">
            <span class="font-bold">{{ partner.userName }}</span>
            <Button @click="selectPartner(partner)">Chat</Button>
        </li>
        </ul>
    </div>

    <div v-if="selectedPartner" class="flex flex-col h-full w-full">
        <h2 class="text-xl font-bold mb-4">{{ selectedPartner.userName }}</h2>

        <div class="mb-4 flex items-center space-x-4">
            <div class="w-[130px]">
                <Select v-model="targetLanguage">
                <SelectTrigger>
                    <SelectValue placeholder="Select language" />
                </SelectTrigger>
                <SelectContent>
                    <SelectItem v-for="lang in languages" :key="lang.code" :value="lang.code">
                    {{ lang.name }}
                    </SelectItem>
                </SelectContent>
                </Select>
            </div>

            <Button 
                @click.prevent="translateAllMessages" 
                :disabled="isTranslating || messages.length === 0" 
                class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:bg-blue-300">
                {{ isTranslating ? 'Translating...' : 'Translate All' }}
            </Button>
        </div>

        <div class="flex-grow overflow-y-auto p-4 pb-20" ref="messagesContainer">
            <div v-for="group in groupedMessages" :key="group.date" class="mb-5 relative">
                <div class="sticky top-0 z-10 flex justify-center mb-2">
                    <span class="bg-white text-gray-700 px-3 py-1 rounded-full text-sm font-semibold shadow-sm">
                        {{ group.date }}
                    </span>
                </div>
                <ul class="list-none p-0 mt-2"> 
                    <li v-for="message in group.messages" :key="message.timeStamp" 
                        :class="{ 'bg-gray-200 ml-auto': message.senderId === currentUser.uid, 'bg-gray-100': message.senderId !== currentUser.uid }"
                        class="mb-2 p-2 rounded-lg max-w-[70%] clear-both">
                        <strong>{{ getUserName(message.senderId) }}</strong>: 
                        {{ message.translatedText || message.text }}
                        <!-- <small v-if="message.translatedText" class="block text-xs text-gray-500">
                            Original: {{ message.text }}
                        </small> -->
                        <small class="block text-xs text-gray-500">{{ formatTime(message.timeStamp) }}</small>
                    </li>
                </ul>
            </div>
        </div>

        <form @submit.prevent="sendMessage" class="flex p-4 bg-gray-100 border-t border-gray-300 fixed bottom-0 left-0 w-full box-border">
        <Input
            v-model="newMessage"
            :id="messageInputId"
            placeholder="Type a message..."
            class="flex-grow mr-2"
        />
        <Button type="submit">Send</Button>
        </form>
        <div v-if="error" class="text-red-500 text-center p-2">{{ error }}</div>
    </div>
    </div>
</div>
</template>


<script setup>
        const languages = [
        { code: 'en', name: 'English' },
        { code: 'es', name: 'Spanish' },
        { code: 'fr', name: 'French' },
        { code: 'de', name: 'German' },
        { code: 'it', name: 'Italian' },
        { code: 'pt', name: 'Portuguese' },
        { code: 'ru', name: 'Russian' },
        { code: 'zh', name: 'Chinese (Simplified)' },
        { code: 'ja', name: 'Japanese' },
        { code: 'ko', name: 'Korean' },
        { code: 'ar', name: 'Arabic' },
        { code: 'hi', name: 'Hindi' },
        { code: 'bn', name: 'Bengali' },
        { code: 'ur', name: 'Urdu' },
        { code: 'tr', name: 'Turkish' },
        { code: 'nl', name: 'Dutch' },
        { code: 'pl', name: 'Polish' },
        { code: 'sv', name: 'Swedish' },
        { code: 'fi', name: 'Finnish' },
        { code: 'da', name: 'Danish' },
        { code: 'no', name: 'Norwegian' },
        { code: 'el', name: 'Greek' },
        { code: 'cs', name: 'Czech' },
        { code: 'th', name: 'Thai' },
        { code: 'vi', name: 'Vietnamese' },
        { code: 'id', name: 'Indonesian' },
        { code: 'ms', name: 'Malay' },
        { code: 'fa', name: 'Persian' },
        { code: 'he', name: 'Hebrew' },
        ]
    import { Button } from "@/components/ui/button"
    import { Input } from "@/components/ui/input"
    import {
        Select,
        SelectContent,
        SelectItem,
        SelectTrigger,
        SelectValue,
        } from "@/components/ui/select"
    import axios from 'axios';
    import { ref, computed, onMounted, watch, nextTick } from 'vue';
    import { auth, db } from '../firebase.js';
    import { onAuthStateChanged } from 'firebase/auth';
    import { collection, setDoc, updateDoc, arrayUnion, onSnapshot, query, where, orderBy, serverTimestamp, getDoc, doc, getDocs } from 'firebase/firestore';

    const currentUser = ref(null);
    const messages = ref([]);
    const newMessage = ref('');
    const error = ref(null);
    const messagesContainer = ref(null);
    const userNames = ref({});
    const selectedPartner = ref(null);
    const availablePartners = ref([]);
    const loading = ref(true);
    const isLoadingPartners = ref(false);
    const rawApiKey = import.meta.env.VITE_GOOGLE_TRANSLATE_API_KEY;
    const cleanApiKey = rawApiKey.replace(/"/g, ''); // Remove any quotation marks
    const apiKey = ref(cleanApiKey.substring(0, cleanApiKey.length / 2)); // Take only the first half to remove duplication

    const targetLanguage = ref('es');
    const isTranslating = ref(false);

    const translateAllMessages = async () => {
    
    if (messages.value.length === 0 || !apiKey.value) {
        error.value = messages.value.length === 0 ? "No messages to translate" : "No API key available for translation";
        return;
    }
    
    isTranslating.value = true;
    
    try {
        const textsToTranslate = messages.value.map(message => message.text);
        console.log("Texts to translate:", textsToTranslate);
        
        const response = await axios.post(
            'https://translation.googleapis.com/language/translate/v2',
            {
                q: textsToTranslate,
                target: targetLanguage.value
            },
            {
                params: {
                    key: apiKey.value
                }
            }
        );
        
        // console.log("Translation response:", response.data);
        
        const translatedTexts = response.data.data.translations.map(t => t.translatedText);
        
        messages.value = messages.value.map((message, index) => ({
            ...message,
            translatedText: translatedTexts[index]
        }));
    } catch (error) {
        console.error('Translation error:', error);
        if (error.response) {
            console.error('Error response:', error.response.data);
            if (error.response.data && error.response.data.error) {
                console.error('Detailed error:', error.response.data.error);
            }
        }
        error.value = `Error: Could not translate messages. ${error.response?.data?.error?.message || error.message}`;
    } finally {
        isTranslating.value = false;
    }
};



    const groupedMessages = computed(() => {
        const groups = {};

        messages.value.forEach(message => {
            const date = new Date(message.timeStamp).toLocaleDateString();
            if (!groups[date]) {
                groups[date] = [];
            }
            groups[date].push(message);
        });
            return Object.entries(groups).map(([date, msgs]) => ({ date, messages: msgs }));
    });



    const sendMessage = async () => {
        error.value = null;
        if (newMessage.value && currentUser.value && selectedPartner.value) {
            const messageObject = {
            senderId: currentUser.value.uid,
            text: newMessage.value,
            timeStamp: Date.now()
            };

            try {
            const messagesRef = collection(db, 'messages');
            const userIds = [currentUser.value.uid, selectedPartner.value.id].sort();
            const chatId = userIds.join('_');

            const chatDocRef = doc(messagesRef, chatId);
            const chatDoc = await getDoc(chatDocRef);

            if (!chatDoc.exists()) {
                // Create a new message document
                await setDoc(chatDocRef, {
                    participants: userIds,
                    messages: [messageObject],
                    lastUpdated: serverTimestamp()
                    });
            } else {
                // Update existing message document
                await updateDoc(chatDocRef, {
                    messages: arrayUnion(messageObject),
                    lastUpdated: serverTimestamp()
                    });
            }

            newMessage.value = '';
            } catch (err) {
                console.error("Error sending message: ", err);
                error.value = "Failed to send message: " + err.message;
            }
        } else {
                error.value = newMessage.value ? "Please select a partner to chat with" : "Cannot send empty message";
        }
    };

    const loadMessages = () => {
        if (!currentUser.value || !selectedPartner.value) {
            console.error("No current user or selected partner");
            return;
        }

        const messagesRef = collection(db, 'messages');
        const userIds = [currentUser.value.uid, selectedPartner.value.id].sort();
        const chatId = userIds.join('_');
        const chatDocRef = doc(messagesRef, chatId);

        const unsubscribe = onSnapshot(chatDocRef, (doc) => {
            if (doc.exists()) {
                const data = doc.data();
                messages.value = data.messages || [];
                console.log("Updated messages:", messages.value);
                nextTick(() => {
                    scrollToBottom();
                });

            messages.value.forEach(message => {
                if (!userNames.value[message.senderId]) {
                fetchUserName(message.senderId);
                }
            });
            }
        }, (err) => {
            console.error("Error loading messages: ", err);
            error.value = "Failed to load messages: " + err.message;
        });

        return unsubscribe;
    };

    const fetchUserName = async (userId) => {
        if (userNames.value[userId]) return;

        try {
        const userDoc = await getDoc(doc(db, 'users', userId));
        if (userDoc.exists()) {
            const userData = userDoc.data();
            userNames.value[userId] = userData.userName || 'Unknown User';
        } else {
            userNames.value[userId] = 'Unknown User';
        }
        } catch (err) {
            console.error("Error fetching username: ", err);
            userNames.value[userId] = 'Unknown User';
        }
    };
        

        const getUserName = (userId) => {
            if (!userNames.value[userId]) {
                fetchUserName(userId);
                return 'Loading...';
            }
            return userNames.value[userId];
    };
        
        const selectPartner = (partner) => {
            selectedPartner.value = partner;
            loadMessages();
        };

        const formatTime = (timeStamp) => {
            return new Date(timeStamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        };  
        
        const scrollToBottom = () => {
            if (messagesContainer.value) {
                messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
            }
        };

        
        onMounted(() => {

        onAuthStateChanged(auth, async (user) => {
            loading.value = true;
            if (user) {
                try {
                    const userDocRef = doc(db, 'users', user.uid);
                    const userDoc = await getDoc(userDocRef);
                    if (userDoc.exists()) {
                        currentUser.value = { 
                            uid: user.uid, 
                            userName: userDoc.data().userName,
                            userType: userDoc.data().userType
                        };
                        loadAvailablePartners();
                    } else {
                        console.error('User document not found in Firestore');
                        currentUser.value = null;
                    }
                } catch (error) {
                    console.error('Error fetching user document:', error);
                    currentUser.value = null;
                }
            } else {
                currentUser.value = null;
            }
            loading.value = false;
        });
    });

        const loadAvailablePartners = async () => {
            if (!currentUser.value) return;

            isLoadingPartners.value = true;
            const usersRef = collection(db, 'users');
            const partnerType = currentUser.value.userType === 'restaurant' ? 'supplier' : 'restaurant';
            const q = query(usersRef, where('userType', '==', partnerType), orderBy('userName'))
            
            try {
                const snapshot = await getDocs(q);
                availablePartners.value = snapshot.docs.map(doc => ({
                id: doc.id,
                userName: doc.data().userName,
                userType: doc.data().userType,
                }));
            } catch (err) {
                console.error("Error loading partners:", err);
                error.value = "Failed to load partners: " + err.message;
            } finally {
                isLoadingPartners.value = false;
            }
            };

            watch(selectedPartner, (newPartner) => {
            if (newPartner) {
                messages.value = []; 
                loadMessages(); 
            }
        });
        const messageInputId = 'message-input';


</script>



