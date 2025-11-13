import ExcelJS from 'exceljs'
import jsPDF from 'jspdf'
import 'jspdf-autotable'

/**
 * Composable pour exporter les devis en Excel et PDF
 */
export function useQuoteExport() {
  /**
   * Exporte les devis au format Excel
   */
  const exportToExcel = async (quotes, filename = 'devis') => {
    if (!quotes || quotes.length === 0) {
      return false
    }

    // Créer le workbook avec ExcelJS
    const workbook = new ExcelJS.Workbook()
    workbook.creator = 'ZSDev'
    workbook.created = new Date()

    const worksheet = workbook.addWorksheet('Devis')

    // Définir les colonnes avec leurs largeurs
    worksheet.columns = [
      { header: 'N° Devis', key: 'quote_number', width: 15 },
      { header: 'Client', key: 'client', width: 25 },
      { header: 'Email', key: 'email', width: 30 },
      { header: 'Téléphone', key: 'phone', width: 15 },
      { header: 'Type de projet', key: 'project_type', width: 25 },
      { header: 'Catégorie', key: 'main_category', width: 20 },
      { header: 'Sous-catégorie', key: 'sub_category', width: 20 },
      { header: 'Montant HT', key: 'total_price', width: 12 },
      { header: 'TVA', key: 'tax_amount', width: 12 },
      { header: 'Remise', key: 'discount', width: 12 },
      { header: 'Montant TTC', key: 'total_price_with_tax', width: 12 },
      { header: 'Statut', key: 'status', width: 15 },
      { header: 'Date création', key: 'created_at', width: 15 },
      { header: 'Date envoi', key: 'sent_date', width: 15 },
      { header: 'Date expiration', key: 'expiry_date', width: 15 },
      { header: 'Notes', key: 'notes', width: 30 }
    ]

    // Styliser l'en-tête
    worksheet.getRow(1).font = { bold: true }
    worksheet.getRow(1).fill = {
      type: 'pattern',
      pattern: 'solid',
      fgColor: { argb: 'FF3b82f6' }
    }
    worksheet.getRow(1).font = { bold: true, color: { argb: 'FFFFFFFF' } }

    // Ajouter les données
    quotes.forEach(quote => {
      worksheet.addRow({
        quote_number: quote.quote_number || '',
        client: quote.client?.user?.first_name && quote.client?.user?.last_name
          ? `${quote.client.user.first_name} ${quote.client.user.last_name}`
          : quote.client?.user?.email || 'N/A',
        email: quote.client?.user?.email || 'N/A',
        phone: quote.client?.phone || 'N/A',
        project_type: quote.project_type?.name || 'N/A',
        main_category: quote.main_category?.name || 'N/A',
        sub_category: quote.sub_category?.name || 'N/A',
        total_price: quote.total_price ? `${parseFloat(quote.total_price).toFixed(2)} €` : '0.00 €',
        tax_amount: quote.tax_amount ? `${parseFloat(quote.tax_amount).toFixed(2)} €` : '0.00 €',
        discount: quote.discount_type === 'percent'
          ? `${quote.discount_value || 0}%`
          : quote.discount_type === 'fixed'
          ? `${quote.discount_value || 0} €`
          : 'N/A',
        total_price_with_tax: quote.total_price_with_tax ? `${parseFloat(quote.total_price_with_tax).toFixed(2)} €` : '0.00 €',
        status: getStatusLabel(quote.status),
        created_at: quote.created_at ? new Date(quote.created_at).toLocaleDateString('fr-FR') : 'N/A',
        sent_date: quote.sent_date ? new Date(quote.sent_date).toLocaleDateString('fr-FR') : 'N/A',
        expiry_date: quote.expiry_date ? new Date(quote.expiry_date).toLocaleDateString('fr-FR') : 'N/A',
        notes: quote.notes || ''
      })
    })

    // Générer et télécharger le fichier
    const timestamp = new Date().toISOString().split('T')[0]
    const buffer = await workbook.xlsx.writeBuffer()
    const blob = new Blob([buffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `${filename}_${timestamp}.xlsx`
    link.click()
    window.URL.revokeObjectURL(url)

    return true
  }

  /**
   * Exporte les devis au format PDF avec statistiques
   */
  const exportToPDF = (quotes, stats = null, filename = 'rapport_devis') => {
    if (!quotes || quotes.length === 0) {
      return false
    }

    const doc = new jsPDF('landscape')
    const pageWidth = doc.internal.pageSize.width
    const pageHeight = doc.internal.pageSize.height

    // En-tête du document
    doc.setFontSize(20)
    doc.setTextColor(37, 99, 235) // Bleu
    doc.text('Rapport des Devis', pageWidth / 2, 20, { align: 'center' })

    doc.setFontSize(10)
    doc.setTextColor(100, 100, 100)
    doc.text(`Généré le ${new Date().toLocaleDateString('fr-FR')} à ${new Date().toLocaleTimeString('fr-FR')}`, pageWidth / 2, 28, { align: 'center' })

    let yPos = 40

    // Statistiques si disponibles
    if (stats) {
      doc.setFontSize(14)
      doc.setTextColor(0, 0, 0)
      doc.text('Statistiques', 14, yPos)
      yPos += 10

      const statsData = [
        ['Total des devis', stats.total || quotes.length],
        ['Brouillons', stats.draft || 0],
        ['Envoyés', stats.sent || 0],
        ['Consultés', stats.viewed || 0],
        ['Acceptés', stats.accepted || 0],
        ['Refusés', stats.rejected || 0],
        ['Expirés', stats.expired || 0],
        ['CA Réalisé', stats.accepted_revenue ? `${parseFloat(stats.accepted_revenue).toFixed(2)} €` : '0.00 €'],
        ['CA En attente', stats.pending_revenue ? `${parseFloat(stats.pending_revenue).toFixed(2)} €` : '0.00 €']
      ]

      doc.autoTable({
        startY: yPos,
        head: [['Indicateur', 'Valeur']],
        body: statsData,
        theme: 'grid',
        headStyles: { fillColor: [37, 99, 235], textColor: 255 },
        styles: { fontSize: 9 },
        margin: { left: 14, right: 14 }
      })

      yPos = doc.lastAutoTable.finalY + 15
    }

    // Liste des devis
    doc.setFontSize(14)
    doc.setTextColor(0, 0, 0)
    doc.text('Liste des Devis', 14, yPos)
    yPos += 5

    const tableData = quotes.map(quote => [
      quote.quote_number || 'N/A',
      quote.client?.user?.first_name && quote.client?.user?.last_name
        ? `${quote.client.user.first_name} ${quote.client.user.last_name}`
        : quote.client?.user?.email || 'N/A',
      quote.project_type?.name || 'N/A',
      quote.total_price ? `${parseFloat(quote.total_price).toFixed(2)} €` : '0.00 €',
      quote.total_price_with_tax ? `${parseFloat(quote.total_price_with_tax).toFixed(2)} €` : '0.00 €',
      getStatusLabel(quote.status),
      quote.created_at ? new Date(quote.created_at).toLocaleDateString('fr-FR') : 'N/A'
    ])

    doc.autoTable({
      startY: yPos,
      head: [['N° Devis', 'Client', 'Type Projet', 'HT', 'TTC', 'Statut', 'Date']],
      body: tableData,
      theme: 'striped',
      headStyles: { fillColor: [37, 99, 235], textColor: 255 },
      styles: { fontSize: 8, cellPadding: 3 },
      columnStyles: {
        0: { cellWidth: 25 },
        1: { cellWidth: 45 },
        2: { cellWidth: 50 },
        3: { cellWidth: 25 },
        4: { cellWidth: 25 },
        5: { cellWidth: 30 },
        6: { cellWidth: 25 }
      },
      margin: { left: 14, right: 14 },
      didDrawPage: (data) => {
        // Pied de page
        doc.setFontSize(8)
        doc.setTextColor(150)
        doc.text(
          `Page ${doc.internal.getNumberOfPages()}`,
          pageWidth / 2,
          pageHeight - 10,
          { align: 'center' }
        )
      }
    })

    // Télécharger le fichier
    const timestamp = new Date().toISOString().split('T')[0]
    doc.save(`${filename}_${timestamp}.pdf`)
    return true
  }

  /**
   * Exporte un devis détaillé en PDF
   */
  const exportQuoteDetailToPDF = (quote) => {
    if (!quote) return false

    const doc = new jsPDF()
    const pageWidth = doc.internal.pageSize.width
    let yPos = 20

    // En-tête
    doc.setFontSize(24)
    doc.setTextColor(37, 99, 235)
    doc.text('DEVIS', pageWidth / 2, yPos, { align: 'center' })
    yPos += 15

    // Numéro de devis
    doc.setFontSize(12)
    doc.setTextColor(0, 0, 0)
    doc.text(`N° ${quote.quote_number || 'N/A'}`, pageWidth / 2, yPos, { align: 'center' })
    yPos += 15

    // Informations client
    doc.setFontSize(14)
    doc.text('Client', 14, yPos)
    yPos += 8

    doc.setFontSize(10)
    const clientName = quote.client?.user?.first_name && quote.client?.user?.last_name
      ? `${quote.client.user.first_name} ${quote.client.user.last_name}`
      : 'N/A'
    doc.text(`Nom: ${clientName}`, 14, yPos)
    yPos += 6
    doc.text(`Email: ${quote.client?.user?.email || 'N/A'}`, 14, yPos)
    yPos += 6
    doc.text(`Téléphone: ${quote.client?.phone || 'N/A'}`, 14, yPos)
    yPos += 6
    doc.text(`Adresse: ${quote.client?.address || 'N/A'}`, 14, yPos)
    yPos += 15

    // Informations projet
    doc.setFontSize(14)
    doc.text('Projet', 14, yPos)
    yPos += 8

    doc.setFontSize(10)
    doc.text(`Type: ${quote.project_type?.name || 'N/A'}`, 14, yPos)
    yPos += 6
    doc.text(`Catégorie: ${quote.main_category?.name || 'N/A'}`, 14, yPos)
    yPos += 6
    if (quote.sub_category) {
      doc.text(`Sous-catégorie: ${quote.sub_category.name}`, 14, yPos)
      yPos += 6
    }
    yPos += 10

    // Articles/Fonctionnalités
    if (quote.quote_items && quote.quote_items.length > 0) {
      doc.setFontSize(14)
      doc.text('Détails', 14, yPos)
      yPos += 5

      const itemsData = quote.quote_items.map(item => [
        item.description || 'N/A',
        item.quantity || 1,
        item.unit_price ? `${parseFloat(item.unit_price).toFixed(2)} €` : '0.00 €',
        item.total_price ? `${parseFloat(item.total_price).toFixed(2)} €` : '0.00 €'
      ])

      doc.autoTable({
        startY: yPos,
        head: [['Description', 'Quantité', 'Prix unitaire', 'Total']],
        body: itemsData,
        theme: 'grid',
        headStyles: { fillColor: [37, 99, 235] },
        styles: { fontSize: 9 }
      })

      yPos = doc.lastAutoTable.finalY + 10
    }

    // Totaux
    doc.setFontSize(12)
    const totalsX = pageWidth - 70
    doc.text('Sous-total HT:', totalsX, yPos)
    doc.text(`${parseFloat(quote.total_price || 0).toFixed(2)} €`, totalsX + 40, yPos, { align: 'right' })
    yPos += 7

    if (quote.discount_value && parseFloat(quote.discount_value) > 0) {
      const discountText = quote.discount_type === 'percent'
        ? `Remise (${quote.discount_value}%):`
        : 'Remise:'
      doc.text(discountText, totalsX, yPos)
      const discountAmount = quote.discount_type === 'percent'
        ? (parseFloat(quote.total_price || 0) * parseFloat(quote.discount_value) / 100)
        : parseFloat(quote.discount_value)
      doc.text(`-${discountAmount.toFixed(2)} €`, totalsX + 40, yPos, { align: 'right' })
      yPos += 7
    }

    doc.text('TVA (20%):', totalsX, yPos)
    doc.text(`${parseFloat(quote.tax_amount || 0).toFixed(2)} €`, totalsX + 40, yPos, { align: 'right' })
    yPos += 10

    doc.setFontSize(14)
    doc.setFont(undefined, 'bold')
    doc.text('Total TTC:', totalsX, yPos)
    doc.text(`${parseFloat(quote.total_price_with_tax || 0).toFixed(2)} €`, totalsX + 40, yPos, { align: 'right' })
    yPos += 15

    // Notes
    if (quote.notes) {
      doc.setFont(undefined, 'normal')
      doc.setFontSize(10)
      doc.text('Notes:', 14, yPos)
      yPos += 6
      const splitNotes = doc.splitTextToSize(quote.notes, pageWidth - 28)
      doc.text(splitNotes, 14, yPos)
    }

    // Télécharger
    doc.save(`devis_${quote.quote_number || 'detail'}.pdf`)
    return true
  }

  /**
   * Obtient le label français du statut
   */
  const getStatusLabel = (status) => {
    const statusLabels = {
      draft: 'Brouillon',
      sent: 'Envoyé',
      viewed: 'Consulté',
      accepted: 'Accepté',
      rejected: 'Refusé',
      expired: 'Expiré'
    }
    return statusLabels[status] || status
  }

  return {
    exportToExcel,
    exportToPDF,
    exportQuoteDetailToPDF
  }
}
