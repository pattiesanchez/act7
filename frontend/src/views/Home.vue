<script setup>
import Header from '@/components/Header.vue';
import Footer from '@/components/Footer.vue';
</script>

<template>
    <Header />
    <div class="breadcumb-area bg-img bg-overlay" style="background-image: url(img/bg-img/breadcumb3.jpg)">
        <div class="container h-100">
            <div class="row h-100 align-items-center">
                <div class="col-12">
                    <div class="breadcumb-text text-center">
                        <h2>Receitas</h2>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <section class="top-catagory-area section-padding-80-0">
        <div class="container">

        </div>
    </section>
    <section class="best-receipe-area">
        <div class="container">
            <div class="row">
                <div class="col-12">
                    <div class="section-heading">
                        <h3>Últimas receitas publicadas</h3>
                    </div>
                </div>
            </div>

            <div class="row">

                <div v-for="(dado, index) in dados.data" :key="index" class="col-12 col-sm-6 col-lg-4">
                    <div class="single-best-receipe-area mb-30">
                        <img :src="dado.imagem" class="foto-mini" :alt="dado.nome" />
                        <div class="receipe-content">
                            <router-link :to="{name:'receitasDetalhes', params:{slug:dado.slug}}">
                                <h5>{{ dado.nome }}</h5>
                            </router-link>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    </section>
    <Footer />
</template>

<style scoped>

</style>