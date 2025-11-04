import * as XLSX from 'xlsx'
import jsPDF from 'jspdf'
import 'jspdf-autotable'

/**
 * Composable pour exporter les devis en Excel et PDF
 */
export function useQuoteExport() {
  /**
   * Exporte les devis au format Excel
   */
  const exportToExcel = (quotes, filename = 'devis') => {
    if (!quotes || quotes.length === 0) {
      return false
    }

    // Préparer les données pour Excel
    const data = quotes.map(quote => ({
      'N° Devis': quote.quote_number || '',
      'Client': quote.client?.user?.first_name && quote.client?.user?.last_name
        ? `${quote.client.user.first_name} ${quote.client.user.last_name}`
        : quote.client?.user?.email || 'N/A',
      'Email': quote.client?.user?.email || 'N/A',
      'Téléphone': quote.client?.phone || 'N/A',
      'Type de projet': quote.project_type?.name || 'N/A',
      'Catégorie': quote.main_category?.name || 'N/A',
      'Sous-catégorie': quote.sub_category?.name || 'N/A',
      'Montant HT': quote.total_price ? `${parseFloat(quote.total_price).toFixed(2)} €` : '0.00 €',
      'TVA': quote.tax_amount ? `${parseFloat(quote.tax_amount).toFixed(2)} €` : '0.00 €',
      'Remise': quote.discount_type === 'percent'
        ? `${quote.discount_value || 0}%`
        : quote.discount_type === 'fixed'
        ? `${quote.discount_value || 0} €`
        : 'N/A',
      'Montant TTC': quote.total_price_with_tax ? `${parseFloat(quote.total_price_with_tax).toFixed(2)} €` : '0.00 €',
      'Statut': getStatusLabel(quote.status),
      'Date création': quote.created_at ? new Date(quote.created_at).toLocaleDateString('fr-FR') : 'N/A',
      'Date envoi': quote.sent_date ? new Date(quote.sent_date).toLocaleDateString('fr-FR') : 'N/A',
      'Date expiration': quote.expiry_date ? new Date(quote.expiry_date).toLocaleDateString('fr-FR') : 'N/A',
      'Notes': quote.notes || ''
    }))

    // Créer le workbook
    const ws = XLSX.utils.json_to_sheet(data)
    const wb = XLSX.utils.book_new()
    XLSX.utils.book_append_sheet(wb, ws, 'Devis')

    // Ajuster la largeur des colonnes
    const colWidths = [
      { wch: 15 }, // N° Devis
      { wch: 25 }, // Client
      { wch: 30 }, // Email
      { wch: 15 }, // Téléphone
      { wch: 25 }, // Type de projet
      { wch: 20 }, // Catégorie
      { wch: 20 }, // Sous-catégorie
      { wch: 12 }, // Montant HT
      { wch: 12 }, // TVA
      { wch: 12 }, // Remise
      { wch: 12 }, // Montant TTC
      { wch: 15 }, // Statut
      { wch: 15 }, // Date création
      { wch: 15 }, // Date envoi
      { wch: 15 }, // Date expiration
      { wch: 30 }  // Notes
    ]
    ws['!cols'] = colWidths

    // Télécharger le fichier
    const timestamp = new Date().toISOString().split('T')[0]
    XLSX.writeFile(wb, `${filename}_${timestamp}.xlsx`)
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
