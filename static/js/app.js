const btnGeneratePrice = document.getElementById("generate-harga");
console.log(btnGeneratePrice);
btnGeneratePrice.addEventListener("click", async (e) => {
    e.preventDefault();
    const luasKos = parseFloat(document.getElementById("luas-kos").value);
    const jarakKampus = parseFloat(document.getElementById("jarak-kampus").value);
    const fasilitas = document.querySelectorAll("#fasilitas");
    let totalFasil = 0;
    fasilitas.forEach((fasil) => {
        if (fasil.checked) {
            totalFasil += parseFloat(fasil.value);
        }
    });

    const response = await fetch("/generate-price", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            luas: luasKos,
            jarak: jarakKampus,
            fasilitas: totalFasil,
        }),
    });
    const result = await response.json()
    let formatRP = new Intl.NumberFormat("id-ID", {
        style: "currency",
        currency: "IDR",
    });
    document.getElementById("hasil").value = formatRP.format(result.result)
});
